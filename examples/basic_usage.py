"""
Basic Usage Examples for ComplianceGuard AI
Simple examples to get started with the system
"""

import asyncio
import json
from typing import Dict, Any

from main import ComplianceGuardAI

class BasicUsageExample:
    """Basic usage examples for ComplianceGuard AI"""
    
    @staticmethod
    async def run_basic_compliance_check():
        """Run a basic compliance check"""
        print("=== Basic Compliance Check Example ===")
        
        # Initialize the system
        compliance_ai = ComplianceGuardAI()
        
        # Sample company data
        company_data = {
            "company_id": "example_company_001",
            "company_name": "Example Technology Corp",
            "industry": "technology",
            "employee_count": 250,
            "revenue_range": "10M-50M",
            "policies": [
                {
                    "name": "Data Protection Policy",
                    "content": "Our company is committed to protecting customer data in accordance with applicable regulations.",
                    "version": "2.0",
                    "last_updated": "2024-01-15"
                },
                {
                    "name": "Information Security Policy",
                    "content": "We implement comprehensive security measures to protect company and customer information.",
                    "version": "1.5", 
                    "last_updated": "2024-02-01"
                }
            ],
            "systems": [
                {
                    "name": "Customer Relationship Management",
                    "data_types": ["customer_data", "contact_information"],
                    "compliance_requirements": ["GDPR", "CCPA"]
                },
                {
                    "name": "Human Resources System",
                    "data_types": ["employee_data", "performance_records"],
                    "compliance_requirements": ["GDPR", "HIPAA"]
                }
            ]
        }
        
        try:
            # Execute compliance check
            print("Executing compliance check...")
            results = await compliance_ai.execute_compliance_check(company_data)
            
            # Display results
            print(f"✓ Compliance check completed!")
            print(f"Workflow ID: {results['workflow_id']}")
            print(f"Overall Compliance Score: {results['report']['executive_summary']['overall_compliance_score']}%")
            print(f"Risk Level: {results['risk_assessment']['risk_level']}")
            print(f"High-priority gaps identified: {len(results['analysis']['gap_analysis'])}")
            
            # Show key recommendations
            print("\nKey Recommendations:")
            for i, action in enumerate(results['report']['recommendations']['immediate_actions'][:3], 1):
                print(f"  {i}. {action['action']} (Priority: {action['priority']})")
                
            return results
            
        except Exception as e:
            print(f"✗ Compliance check failed: {e}")
            return None
        
        finally:
            await compliance_ai.shutdown()
    
    @staticmethod
    async def run_multiple_companies():
        """Run compliance checks for multiple companies"""
        print("\n=== Multiple Companies Example ===")
        
        companies = [
            {
                "company_id": "tech_company_001",
                "company_name": "Tech Startup Inc",
                "industry": "technology",
                "employee_count": 50,
                "policies": [{"name": "Basic Data Policy", "content": "Simple data protection policy"}]
            },
            {
                "company_id": "health_company_001", 
                "company_name": "Healthcare Provider LLC",
                "industry": "healthcare",
                "employee_count": 200,
                "policies": [{"name": "Patient Data Policy", "content": "HIPAA compliant patient data handling"}]
            },
            {
                "company_id": "finance_company_001",
                "company_name": "Financial Services Corp", 
                "industry": "finance",
                "employee_count": 150,
                "policies": [{"name": "Financial Compliance Policy", "content": "SOX and financial regulations"}]
            }
        ]
        
        compliance_ai = ComplianceGuardAI()
        results = []
        
        try:
            for company in companies:
                print(f"Checking compliance for {company['company_name']}...")
                result = await compliance_ai.execute_compliance_check(company)
                results.append(result)
                
                score = result['report']['executive_summary']['overall_compliance_score']
                print(f"  ✓ {company['company_name']}: {score}% compliance")
            
            # Summary
            print(f"\nSummary: Checked {len(results)} companies")
            avg_score = sum(r['report']['executive_summary']['overall_compliance_score'] for r in results) / len(results)
            print(f"Average compliance score: {avg_score:.1f}%")
            
            return results
            
        finally:
            await compliance_ai.shutdown()
    
    @staticmethod
    async def demo_continuous_monitoring():
        """Demonstrate continuous monitoring"""
        print("\n=== Continuous Monitoring Demo ===")
        
        compliance_ai = ComplianceGuardAI()
        
        try:
            # Start continuous monitoring
            print("Starting continuous compliance monitoring...")
            monitoring_task = asyncio.create_task(compliance_ai.start_continuous_monitoring())
            
            # Let it run for a short time
            print("Monitoring running for 10 seconds...")
            await asyncio.sleep(10)
            
            # Stop monitoring
            print("Stopping monitoring...")
            await compliance_ai.shutdown()
            monitoring_task.cancel()
            
            print("✓ Continuous monitoring demo completed")
            
        except Exception as e:
            print(f"✗ Monitoring demo failed: {e}")
            await compliance_ai.shutdown()

async def main():
    """Run all basic usage examples"""
    example = BasicUsageExample()
    
    # Run basic compliance check
    await example.run_basic_compliance_check()
    
    # Run multiple companies
    await example.run_multiple_companies()
    
    # Demo continuous monitoring
    await example.demo_continuous_monitoring()

if __name__ == "__main__":
    asyncio.run(main())