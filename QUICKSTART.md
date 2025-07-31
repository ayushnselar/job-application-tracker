# Quick Start Guide - Job Application Tracker

Get your job application tracker up and running in 10 minutes!

## Prerequisites

- AWS CLI configured
- AWS SAM CLI installed
- Google Service Account with Editor access to a Google Sheet

## Step 1: Create Google Sheet

Create a Google Sheet with these columns in order:
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

## Step 2: Store Google Credentials

```bash
aws secretsmanager create-secret \
    --name "google-service-account" \
    --description "Google Service Account credentials" \
    --secret-string file://path/to/your/service-account-key.json
```

## Step 3: Update Configuration

Edit `template.yaml` and replace:
- `{{PLACEHOLDER_GOOGLE_CREDENTIALS_SECRET_ARN}}` with your secret ARN
- `{{PLACEHOLDER_GOOGLE_SHEET_ID}}` with your Google Sheet ID

## Step 4: Deploy

```bash
./deploy.sh
```

## Step 5: Test

```bash
curl -X POST https://your-api-gateway-url/prod/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.linkedin.com/jobs/view/example-job"}'
```

## That's it! 🎉

Your job application tracker is now running. Send job URLs to the API endpoint and they'll be automatically scraped and logged to your Google Sheet.

## Troubleshooting

- **Permission errors**: Check that your Google Service Account has Editor access
- **Deployment fails**: Verify AWS CLI is configured correctly
- **Scraping fails**: Check if the website structure has changed

## Next Steps

- Customize CSS selectors in `config.py` for different job sites
- Add more error handling as needed
- Monitor CloudWatch logs for any issues 