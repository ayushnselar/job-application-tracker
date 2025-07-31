import json
import logging
import boto3
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
from config import GOOGLE_SHEET_COLUMNS

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
secretsmanager = boto3.client('secrets-manager')

def lambda_handler(event, context):
    """
    Lambda function to process SQS messages and upload job data to Google Sheets.
    
    Expected event format (SQS event):
    {
        "Records": [
            {
                "body": "{\"company\": \"...\", \"role\": \"...\", ...}"
            }
        ]
    }
    """
    try:
        # Process each SQS record
        for record in event['Records']:
            process_sqs_record(record)
            
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Successfully processed all records'})
        }
        
    except Exception as e:
        logger.error(f"Error processing SQS records: {str(e)}")
        # Don't return error response for SQS Lambda - let it retry
        raise

def process_sqs_record(record):
    """
    Process a single SQS record and upload to Google Sheets.
    
    Args:
        record (dict): SQS record containing job data
    """
    try:
        # Parse the message body
        job_data = json.loads(record['body'])
        logger.info(f"Processing job data for company: {job_data.get('company', 'Unknown')}")
        
        # Get Google Sheets credentials from Secrets Manager
        credentials = get_google_credentials()
        
        # Upload to Google Sheets
        upload_to_sheets(job_data, credentials)
        
        logger.info(f"Successfully uploaded job data for {job_data.get('company', 'Unknown')}")
        
    except Exception as e:
        logger.error(f"Error processing record: {str(e)}")
        # Re-raise to trigger SQS retry
        raise

def get_google_credentials():
    """
    Retrieve Google Service Account credentials from AWS Secrets Manager.
    
    Returns:
        Credentials: Google OAuth2 credentials object
    """
    try:
        # Get secret ARN from environment variable
        secret_arn = os.environ.get('GOOGLE_CREDENTIALS_SECRET_ARN')
        if not secret_arn:
            raise ValueError("GOOGLE_CREDENTIALS_SECRET_ARN environment variable not set")
        
        # Retrieve the secret
        response = secretsmanager.get_secret_value(SecretId=secret_arn)
        secret_string = response['SecretString']
        
        # Parse the JSON credentials
        credentials_info = json.loads(secret_string)
        
        # Create credentials object
        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        return credentials
        
    except Exception as e:
        logger.error(f"Error retrieving Google credentials: {str(e)}")
        raise

def upload_to_sheets(job_data, credentials):
    """
    Upload job data to Google Sheets.
    
    Args:
        job_data (dict): Job data to upload
        credentials: Google OAuth2 credentials
    """
    try:
        # Get sheet ID from environment variable
        sheet_id = os.environ.get('GOOGLE_SHEET_ID')
        if not sheet_id:
            raise ValueError("GOOGLE_SHEET_ID environment variable not set")
        
        # Authenticate with Google Sheets
        gc = gspread.authorize(credentials)
        
        # Open the spreadsheet
        spreadsheet = gc.open_by_key(sheet_id)
        
        # Get the first worksheet (or specify by name if needed)
        worksheet = spreadsheet.get_worksheet(0)
        if not worksheet:
            worksheet = spreadsheet.sheet1
        
        # Prepare row data in the correct order based on configuration
        row_data = []
        for column in GOOGLE_SHEET_COLUMNS:
            # Map column names to job_data keys
            column_mapping = {
                'Company': 'company',
                'Role': 'role',
                'Job Posting': 'job_posting',
                'Application Date': 'application_date',
                'Location': 'location',
                'Status': 'status',
                'Contact(s)': 'contacts',
                'Notes': 'notes',
                'Offer': 'offer',
                'Resume': 'resume',
                'Interest': 'interest'
            }
            
            key = column_mapping.get(column, column.lower())
            value = job_data.get(key, 'N/A')
            row_data.append(value)
        
        # Append the row to the sheet
        worksheet.append_row(row_data)
        
        logger.info(f"Successfully appended row to Google Sheet: {row_data[:3]}...")  # Log first 3 columns
        
    except Exception as e:
        logger.error(f"Error uploading to Google Sheets: {str(e)}")
        raise 