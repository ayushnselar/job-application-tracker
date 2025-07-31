# Job Application Tracker - Serverless Pipeline

A serverless pipeline for automating job application tracking. This project demonstrates AWS serverless architecture, web scraping, and integration with Google Sheets.

## 🎯 Project Overview

### Core Functionality
- **Web Scraping**: Automatically extracts job details from posting URLs
- **Data Processing**: Parses company, role, and location information
- **Google Sheets Integration**: Logs data to a structured spreadsheet
- **Serverless Architecture**: Scalable, cost-effective AWS Lambda-based solution

### Key Features
- **Zero Infrastructure Management**: Fully serverless architecture
- **Automatic Scaling**: Handles varying load with AWS Lambda
- **Error Handling**: Robust retry mechanisms and error logging
- **Easy Deployment**: Infrastructure as Code with AWS SAM

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │───▶│  Scraper Lambda  │───▶│  SQS Queue      │───▶│ Uploader Lambda │
│   (HTTP POST)   │    │  (scraper.py)    │    │                 │    │ (uploader.py)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │                        │
                                                       ▼                        ▼
                                              ┌─────────────────┐    ┌─────────────────┐
                                              │  Dead Letter    │    │  Google Sheets  │
                                              │     Queue       │    │                 │
                                              └─────────────────┘    └─────────────────┘
```

### Components:

1. **API Gateway**: Accepts HTTP POST requests with job URLs
2. **Scraper Lambda**: Extracts job details using web scraping
3. **SQS Queue**: Decouples scraping from uploading for reliability
4. **Uploader Lambda**: Writes data to Google Sheets
5. **Dead Letter Queue**: Handles failed messages for retry
6. **Google Sheets**: Stores job application data

## 📋 Prerequisites

- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Google Service Account with Editor access to your Google Sheet
- Python 3.11+ (for local development)

## 🚀 Setup Instructions

### 1. Prepare Your Google Sheet

Create a Google Sheet with the following columns in order:
- Company
- Role  
- Job Posting
- Application Date
- Location
- Status
- Contact(s)
- Notes
- Offer
- Resume
- Interest

### 2. Store Google Credentials in AWS Secrets Manager

```bash
# Create a secret with your Google Service Account JSON
aws secretsmanager create-secret \
    --name "google-service-account" \
    --description "Google Service Account credentials for Job Tracker" \
    --secret-string file://path/to/your/service-account-key.json
```

### 3. Update Configuration

Edit `template.yaml` and replace the placeholders:
- `{{PLACEHOLDER_GOOGLE_CREDENTIALS_SECRET_ARN}}`: Your secret ARN from step 2
- `{{PLACEHOLDER_GOOGLE_SHEET_ID}}`: Your Google Sheet ID (from the URL)

### 4. Deploy the Application

```bash
# Build and deploy
sam build
sam deploy --guided
```

## 🧪 Testing

### Test the API Endpoint

```bash
# Get your API Gateway URL from the deployment output
curl -X POST https://your-api-gateway-url/prod/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.linkedin.com/jobs/view/example-job"}'
```

### Local Testing

```bash
# Test the scraper function locally
python test_local.py
```

## 📁 Project Structure

```
job-application-tracker/
├── scraper.py          # Lambda function for web scraping
├── uploader.py         # Lambda function for Google Sheets upload
├── config.py           # Configuration settings
├── template.yaml       # AWS SAM infrastructure template
├── requirements.txt    # Python dependencies
├── test_local.py       # Local testing script
├── deploy.sh           # Deployment convenience script
├── README.md           # This file
└── QUICKSTART.md       # Quick setup guide
```

## 🔧 Configuration

### CSS Selectors

The scraper uses configurable CSS selectors in `config.py`:

```python
CSS_SELECTORS = {
    'default': {
        'company': 'div.company-name',
        'role': 'h1.job-title', 
        'location': 'span.job-location'
    },
    'linkedin.com': {
        'company': '.job-details-jobs-unified-top-card__company-name',
        'role': '.job-details-jobs-unified-top-card__job-title',
        'location': '.job-details-jobs-unified-top-card__bullet'
    }
}
```

### Request Settings

Configure request headers and timeouts:

```python
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
REQUEST_TIMEOUT = 30
```

## 🚨 Error Handling

The application includes comprehensive error handling:

- **Network Errors**: Retries with exponential backoff
- **Parsing Errors**: Graceful fallback to default values
- **SQS Failures**: Dead letter queue for failed messages
- **Google Sheets Errors**: Detailed logging and retry logic

## 📊 Monitoring

Basic monitoring is provided through AWS CloudWatch:

- Lambda function execution logs
- SQS queue metrics
- API Gateway request logs
- Error tracking and alerting

## 🔒 Security

- **IAM Roles**: Least privilege access for each Lambda function
- **Secrets Manager**: Secure storage of Google credentials
- **Input Validation**: URL format and domain validation
- **Error Logging**: No sensitive data in logs

## 🚀 Deployment

### Quick Deploy

```bash
./deploy.sh
```

### Manual Deploy

```bash
sam build
sam deploy --guided
```

## 🧪 Development

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Test locally:
```bash
python test_local.py
```

3. Use AWS SAM for local testing:
```bash
sam local invoke ScraperFunction --event events/test-event.json
```

## 📈 Scaling

The application automatically scales based on demand:

- **API Gateway**: Handles concurrent requests
- **Lambda**: Auto-scales based on SQS queue depth
- **SQS**: Buffers messages during high load
- **Google Sheets**: Handles batch operations efficiently

## 🛠️ Troubleshooting

### Common Issues

1. **Google Sheets Permission Error**
   - Verify service account has Editor access
   - Check sheet ID is correct

2. **SQS Message Not Processing**
   - Check CloudWatch logs for Lambda errors
   - Verify IAM permissions

3. **Scraping Failures**
   - Check if website structure changed
   - Update CSS selectors in config.py

### Debug Mode

Enable detailed logging by setting `LOG_LEVEL=DEBUG` in the Lambda environment variables.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AWS SAM for serverless infrastructure
- BeautifulSoup for web scraping
- gspread for Google Sheets integration
- The open-source community for inspiration and tools
