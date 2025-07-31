#!/bin/bash

# Job Application Tracker Deployment Script
# This script builds and deploys the serverless application

set -e  # Exit on any error

echo "🚀 Starting deployment of Job Application Tracker..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ AWS SAM CLI is not installed. Please install it first."
    echo "   Visit: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Build the application
echo "🔨 Building SAM application..."
sam build

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully"
else
    echo "❌ Build failed"
    exit 1
fi

# Deploy the application
echo "🚀 Deploying to AWS..."
sam deploy --guided

if [ $? -eq 0 ]; then
    echo "✅ Deployment completed successfully!"
    echo ""
    echo "🎉 Your Job Application Tracker is now live!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Update the Google credentials secret ARN in template.yaml"
    echo "2. Update the Google Sheet ID in template.yaml"
    echo "3. Test the API endpoint with a job URL"
    echo ""
    echo "🔗 API Gateway URL will be displayed above"
else
    echo "❌ Deployment failed"
    exit 1
fi 