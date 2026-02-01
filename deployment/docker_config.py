"""
Docker Configuration for ComplianceGuard AI
Containerization setup for the multi-agent system
"""

import os
from typing import Dict, Any

class DockerConfig:
    """Docker configuration for ComplianceGuard AI deployment"""
    
    @staticmethod
    def generate_dockerfile() -> str:
        """Generate Dockerfile for ComplianceGuard AI"""
        return """# ComplianceGuard AI Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 agentuser && chown -R agentuser:agentuser /app
USER agentuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Start command
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
"""

    @staticmethod
    def generate_docker_compose() -> str:
        """Generate docker-compose.yml for local development"""
        return """# ComplianceGuard AI Docker Compose
version: '3.8'

services:
  complianceguard-ai:
    build: .
    ports:
      - "8080:8080"
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account.json
      - LOG_LEVEL=INFO
    volumes:
      - ./credentials:/app/credentials:ro
      - ./config:/app/config:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
"""

    @staticmethod
    def generate_build_script() -> str:
        """Generate build script for Docker image"""
        return """#!/bin/bash
# ComplianceGuard AI Docker Build Script

set -e

# Configuration
IMAGE_NAME="complianceguard-ai"
VERSION="1.0.0"
REGISTRY="gcr.io/your-project-id"

echo "Building ComplianceGuard AI Docker image..."

# Build the image
docker build -t $IMAGE_NAME:$VERSION -t $IMAGE_NAME:latest .

# Tag for registry
docker tag $IMAGE_NAME:$VERSION $REGISTRY/$IMAGE_NAME:$VERSION
docker tag $IMAGE_NAME:latest $REGISTRY/$IMAGE_NAME:latest

echo "Build complete!"
echo "Images:"
echo "  - $IMAGE_NAME:$VERSION"
echo "  - $REGISTRY/$IMAGE_NAME:$VERSION"
echo ""
echo "To push to registry:"
echo "  docker push $REGISTRY/$IMAGE_NAME:$VERSION"
echo "  docker push $REGISTRY/$IMAGE_NAME:latest"
"""