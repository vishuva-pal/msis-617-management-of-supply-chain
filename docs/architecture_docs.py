"""
Architecture Documentation for ComplianceGuard AI
System architecture, design patterns, and technical overview
"""

class ArchitectureDocumentation:
    """Architecture documentation generator"""
    
    @staticmethod
    def generate_architecture_overview() -> str:
        """Generate system architecture overview"""
        return """
# ComplianceGuard AI - System Architecture

## Overview
ComplianceGuard AI is a multi-agent system designed to automate enterprise compliance across multiple regulatory frameworks including GDPR, HIPAA, and SOX. The system uses intelligent agent coordination to provide real-time compliance monitoring, automated gap analysis, and instant reporting.

## Core Architecture Principles

### 1. Multi-Agent System Design
- **Agent Specialization**: Each agent has a specific domain expertise
- **Sequential Workflow**: Data flows through agents in a structured pipeline
- **Parallel Processing**: Multiple compliance checks run simultaneously
- **Loop Monitoring**: Continuous regulatory change detection

### 2. Microservices Architecture
- **Containerized Deployment**: Docker-based containerization
- **Cloud-Native**: Designed for Google Cloud Run and Kubernetes
- **API-First**: RESTful APIs for all external integrations
- **Stateless Design**: Session management for state preservation

### 3. AI-Powered Intelligence
- **Gemini Integration**: Google's Gemini models for complex reasoning
- **Custom Tools**: Specialized compliance analysis tools
- **Memory Management**: Long-term context preservation
- **Adaptive Learning**: Continuous improvement from compliance patterns

## System Components

### Agent Layer """