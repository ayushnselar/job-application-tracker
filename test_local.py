#!/usr/bin/env python3
"""
Local testing script for the Job Application Tracker scraper function.
This script allows you to test the scraper locally before deploying to AWS.
"""

import json
import sys
import os
from scraper import lambda_handler

def test_scraper():
    """Test the scraper function with a sample job URL."""
    
    # Sample job URL - replace with a real job posting URL for testing
    test_url = "https://example.com/job-posting"
    
    # If a URL is provided as command line argument, use it
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    
    print(f"🧪 Testing scraper with URL: {test_url}")
    print("=" * 50)
    
    # Create test event
    test_event = {
        "url": test_url
    }
    
    try:
        # Mock the SQS_QUEUE_URL environment variable for local testing
        os.environ['SQS_QUEUE_URL'] = 'http://localhost:4566/000000000000/test-queue'
        
        # Call the lambda handler
        result = lambda_handler(test_event, None)
        
        print("✅ Scraper function executed successfully!")
        print(f"Status Code: {result.get('statusCode')}")
        
        # Parse and display the response body
        if 'body' in result:
            body = json.loads(result['body'])
            print("\n📊 Scraped Job Data:")
            print("-" * 30)
            
            if 'jobData' in body:
                job_data = body['jobData']
                for key, value in job_data.items():
                    print(f"{key:20}: {value}")
            else:
                print("No job data found in response")
                
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Error testing scraper: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False
    
    return True

def test_with_sample_html():
    """Test the scraper with a sample HTML page."""
    
    print("🧪 Testing with sample HTML (this will fail as expected)")
    print("=" * 50)
    
    # This will fail because example.com doesn't have the expected CSS selectors
    # but it's useful for testing error handling
    test_event = {
        "url": "https://example.com"
    }
    
    try:
        os.environ['SQS_QUEUE_URL'] = 'http://localhost:4566/000000000000/test-queue'
        result = lambda_handler(test_event, None)
        
        print("✅ Function executed (expected to return N/A values)")
        print(f"Status Code: {result.get('statusCode')}")
        
        if 'body' in result:
            body = json.loads(result['body'])
            if 'jobData' in body:
                job_data = body['jobData']
                print("\n📊 Scraped Data (should show N/A values):")
                print("-" * 30)
                for key, value in job_data.items():
                    print(f"{key:20}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Job Application Tracker - Local Testing")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Test with provided URL
        success = test_scraper()
        if not success:
            sys.exit(1)
    else:
        # Test with sample HTML
        test_with_sample_html()
        print("\n💡 To test with a real job URL, run:")
        print("   python test_local.py 'https://real-job-posting-url.com'")
    
    print("\n✅ Testing completed!") 