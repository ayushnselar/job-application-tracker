"""
Configuration file for Job Application Tracker
Update these values according to your setup and target websites.
"""

# AWS Configuration
AWS_REGION = "us-east-1"  # Change to your preferred region

# Google Sheets Configuration
GOOGLE_SHEET_COLUMNS = [
    "Company",
    "Role", 
    "Job Posting",
    "Application Date",
    "Location",
    "Status",
    "Contact(s)",
    "Notes",
    "Offer",
    "Resume",
    "Interest"
]

# CSS Selectors for different job sites
# Add more selectors for different websites as needed
CSS_SELECTORS = {
    "default": {
        "company": "div.company-name",
        "role": "h1.job-title", 
        "location": "span.job-location"
    },
    # Example for LinkedIn job postings
    "linkedin.com": {
        "company": ".job-details-jobs-unified-top-card__company-name",
        "role": ".job-details-jobs-unified-top-card__job-title",
        "location": ".job-details-jobs-unified-top-card__bullet"
    },
    # Example for Indeed job postings  
    "indeed.com": {
        "company": "[data-testid='jobsearch-CompanyInfoContainer'] h2",
        "role": "[data-testid='jobsearch-JobInfoHeader-title']",
        "location": "[data-testid='jobsearch-JobInfoHeader-locationText']"
    }
}

# HTTP Request Configuration
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

REQUEST_TIMEOUT = 30  # seconds

# Default values for missing data
DEFAULT_VALUES = {
    "status": "To Apply",
    "contacts": "N/A",
    "notes": "N/A", 
    "offer": "N/A",
    "resume": "N/A",
    "interest": "N/A"
}

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# SQS Configuration
SQS_VISIBILITY_TIMEOUT = 300  # 5 minutes
SQS_MESSAGE_RETENTION = 1209600  # 14 days
SQS_MAX_RECEIVE_COUNT = 3  # Number of retries before message goes to DLQ

# Lambda Configuration
LAMBDA_TIMEOUT = 60  # seconds
LAMBDA_MEMORY_SIZE = 512  # MB 