import json
import logging
import boto3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
import os
import time
from config import CSS_SELECTORS, REQUEST_HEADERS, REQUEST_TIMEOUT, DEFAULT_VALUES

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    """
    Lambda function to scrape job details from a URL and publish to SQS queue.
    
    Expected event format:
    {
        "url": "https://example.com/job-posting"
    }
    """
    start_time = time.time()
    
    try:
        # Parse the incoming request
        if 'body' in event:
            # API Gateway wraps the body in a 'body' field
            body = json.loads(event['body'])
        else:
            body = event
            
        job_url = body.get('url')
        
        if not job_url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required in request body'})
            }
        
        logger.info(f"Scraping job details from: {job_url}")
        
        # Scrape job details with timing
        scrape_start = time.time()
        job_data = scrape_job_details(job_url)
        scrape_duration = (time.time() - scrape_start) * 1000  # Convert to milliseconds
        
        # Add metadata
        job_data['job_url'] = job_url
        job_data['scraped_at'] = datetime.now().isoformat()
        
        # Publish to SQS queue
        queue_url = os.environ.get('SQS_QUEUE_URL')
        if not queue_url:
            raise ValueError("SQS_QUEUE_URL environment variable not set")
        
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(job_data)
        )
        
        total_duration = (time.time() - start_time) * 1000
        
        logger.info(f"Successfully published job data to SQS. MessageId: {response['MessageId']}, Duration: {total_duration:.2f}ms")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Job details scraped and queued successfully',
                'messageId': response['MessageId'],
                'jobData': job_data,
                'duration_ms': round(total_duration, 2)
            })
        }
        
    except requests.RequestException as e:
        logger.error(f"Network error while scraping: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Network error: {str(e)}'})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }

def scrape_job_details(url):
    """
    Scrape job details from the given URL using BeautifulSoup.
    
    Args:
        url (str): The job posting URL to scrape
        
    Returns:
        dict: Dictionary containing scraped job details
    """
    # Determine which selectors to use based on the domain
    domain = urlparse(url).netloc.lower()
    selectors = CSS_SELECTORS.get(domain, CSS_SELECTORS['default'])
    
    # Make the request
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract job details using the appropriate selectors
    company = extract_text(soup, selectors['company'])
    role = extract_text(soup, selectors['role'])
    location = extract_text(soup, selectors['location'])
    
    # Get current date for application date
    application_date = datetime.now().strftime('%Y-%m-%d')
    
    return {
        'company': company,
        'role': role,
        'job_posting': url,
        'application_date': application_date,
        'location': location,
        'status': DEFAULT_VALUES['status'],
        'contacts': DEFAULT_VALUES['contacts'],
        'notes': DEFAULT_VALUES['notes'],
        'offer': DEFAULT_VALUES['offer'],
        'resume': DEFAULT_VALUES['resume'],
        'interest': DEFAULT_VALUES['interest']
    }

def extract_text(soup, selector):
    """
    Extract text from an HTML element using CSS selector.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object
        selector (str): CSS selector
        
    Returns:
        str: Extracted text or "N/A" if not found
    """
    try:
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
        else:
            return "N/A"
    except Exception as e:
        logger.warning(f"Error extracting text with selector '{selector}': {str(e)}")
        return "N/A" 