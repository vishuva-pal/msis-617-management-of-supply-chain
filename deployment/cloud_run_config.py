"""
Google Cloud Run Configuration
Deployment configuration for serverless container execution
"""

from typing import Dict, Any

class CloudRunConfig:
    """Cloud Run deployment configuration"""
    
    @staticmethod
    def generate_service_yaml() -> str:
        """Generate Cloud Run service configuration"""
        return """# ComplianceGuard AI Cloud Run Service
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: complianceguard-ai
  labels:
    app: complianceguard-ai
    version: v1
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: '10'
        autoscaling.knative.dev/minScale: '1'
    spec:
      containerConcurrency: 10
      timeoutSeconds: 300
      containers:
      - image: gcr.io/your-project-id/complianceguard-ai:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: 2000m
            memory: 4Gi
          requests:
            cpu: 1000m
            memory: 2Gi
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: "/app/credentials/service-account.json"
        - name: REDIS_HOST
          value: "your-redis-host"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
"""

    @staticmethod
    def generate_deployment_script() -> str:
        """Generate deployment script for Cloud Run"""
        return """#!/bin/bash
# ComplianceGuard AI Cloud Run Deployment Script

set -e

# Configuration
PROJECT_ID="your-project-id"
REGION="us-central1"
SERVICE_NAME="complianceguard-ai"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying ComplianceGuard AI to Cloud Run..."

# Build and push Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME:latest .

echo "Pushing image to Container Registry..."
docker push $IMAGE_NAME:latest

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \\
  --image $IMAGE_NAME:latest \\
  --platform managed \\
  --region $REGION \\
  --cpu 2 \\
  --memory 4Gi \\
  --min-instances 1 \\
  --max-instances 10 \\
  --concurrency 10 \\
  --timeout 300 \\
  --allow-unauthenticated \\
  --set-env-vars="LOG_LEVEL=INFO" \\
  --set-env-vars="GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account.json"

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo ""
echo "Deployment complete!"
echo "Service URL: $SERVICE_URL"
echo ""
echo "To test the deployment:"
echo "  curl $SERVICE_URL/health"
echo "  curl -X POST $SERVICE_URL/api/compliance-check -H 'Content-Type: application/json' -d '@sample_data.json'"
"""

    @staticmethod
    def generate_ci_cd_yaml() -> str:
        """Generate GitHub Actions CI/CD pipeline"""
        return """# ComplianceGuard AI CI/CD Pipeline
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  SERVICE_NAME: complianceguard-ai
  REGION: us-central1

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
        
    - name: Run tests
      run: |
        pytest tests/ -v --cov=.
        
  deploy:
    name: Deploy to Cloud Run
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Google Auth
      uses: 'google-github-actions/auth@v1'
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'
        
    - name: Set up Cloud SDK
      uses: 'google-github-actions/setup-gcloud@v1'
      
    - name: Configure Docker
      run: gcloud auth configure-docker
      
    - name: Build and Push Container
      run: |
        docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:${{ github.sha }} .
        docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:${{ github.sha }}
        
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy $SERVICE_NAME \\
          --image gcr.io/$PROJECT_ID/$SERVICE_NAME:${{ github.sha }} \\
          --platform managed \\
          --region $REGION \\
          --cpu 2 \\
          --memory 4Gi \\
          --min-instances 1 \\
          --max-instances 10 \\
          --allow-unauthenticated
"""