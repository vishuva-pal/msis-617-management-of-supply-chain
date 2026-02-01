"""
Sample Data for ComplianceGuard AI
Sample company data and test cases
"""

from typing import Dict, Any, List

class SampleData:
    """Sample data for testing and demonstration"""
    
    @staticmethod
    def get_sample_company_data() -> Dict[str, Any]:
        """Get sample company data for testing"""
        return {
            "company_id": "sample_company_001",
            "company_name": "Sample Technology Corporation",
            "industry": "technology",
            "employee_count": 500,
            "revenue_range": "50M-100M",
            "operating_regions": ["US", "EU", "APAC"],
            "compliance_requirements": ["GDPR", "HIPAA", "SOX", "CCPA"],
            "policies": [
                {
                    "name": "Data Protection and Privacy Policy",
                    "content": """
                    This policy outlines our commitment to protecting personal data in compliance with global privacy regulations.
                    
                    Key Principles:
                    - Data minimization: We only collect necessary data
                    - Purpose limitation: Data used only for specified purposes
                    - Storage limitation: Data retained only as long as necessary
                    - Integrity and confidentiality: Appropriate security measures
                    
                    Data Subject Rights:
                    - Right to access personal data
                    - Right to rectification of inaccurate data
                    - Right to erasure ('right to be forgotten')
                    - Right to data portability
                    - Right to object to processing
                    
                    Data Breach Response:
                    - Immediate assessment of breach scope
                    - Notification to authorities within 72 hours
                    - Communication to affected individuals
                    - Implementation of remediation measures
                    """,
                    "version": "3.1",
                    "last_updated": "2024-03-15",
                    "status": "active"
                },
                {
                    "name": "Information Security Policy",
                    "content": """
                    Comprehensive security framework to protect company and customer information.
                    
                    Security Controls:
                    - Access control: Role-based access with principle of least privilege
                    - Encryption: Data encrypted at rest and in transit
                    - Network security: Firewalls, intrusion detection, VPN
                    - Physical security: Secure facilities, access logs
                    - Incident response: Documented procedures for security incidents
                    
                    Employee Training:
                    - Annual security awareness training
                    - Phishing simulation exercises
                    - Secure coding practices for developers
                    - Data handling procedures for all staff
                    
                    Third-Party Risk Management:
                    - Vendor security assessments
                    - Contractual security requirements
                    - Regular security audits
                    """,
                    "version": "2.2",
                    "last_updated": "2024-02-28",
                    "status": "active"
                },
                {
                    "name": "Employee Data Protection Policy",
                    "content": """
                    Guidelines for handling employee personal data in compliance with employment regulations.
                    
                    Employee Data Categories:
                    - Personal identification information
                    - Employment history and performance
                    - Compensation and benefits data
                    - Health and medical information (where applicable)
                    - Background check information
                    
                    Data Processing:
                    - Explicit consent obtained for sensitive data
                    - Limited access to HR personnel only
                    - Secure storage with encryption
                    - Regular data purging for former employees
                    """,
                    "version": "1.8",
                    "last_updated": "2024-01-10",
                    "status": "active"
                }
            ],
            "systems": [
                {
                    "name": "Customer Relationship Management (CRM)",
                    "type": "cloud_saas",
                    "vendor": "Salesforce",
                    "data_categories": [
                        "customer_contact_information",
                        "sales_history", 
                        "communication_records",
                        "marketing_preferences"
                    ],
                    "compliance_requirements": ["GDPR", "CCPA"],
                    "data_retention_period": "36 months",
                    "encryption_status": "encrypted_at_rest_and_transit"
                },
                {
                    "name": "Human Resources Information System (HRIS)",
                    "type": "cloud_saas", 
                    "vendor": "Workday",
                    "data_categories": [
                        "employee_personal_information",
                        "compensation_data",
                        "performance_reviews",
                        "benefits_enrollment"
                    ],
                    "compliance_requirements": ["GDPR", "HIPAA"],
                    "data_retention_period": "7 years post-employment",
                    "encryption_status": "encrypted_at_rest_and_transit"
                },
                {
                    "name": "Financial Management System",
                    "type": "on_premises",
                    "vendor": "SAP",
                    "data_categories": [
                        "financial_transactions",
                        "accounting_records", 
                        "audit_trails",
                        "tax_documents"
                    ],
                    "compliance_requirements": ["SOX"],
                    "data_retention_period": "10 years",
                    "encryption_status": "encrypted_at_rest"
                },
                {
                    "name": "Internal Communication Platform",
                    "type": "cloud_saas",
                    "vendor": "Slack",
                    "data_categories": [
                        "internal_communications",
                        "file_sharing",
                        "collaboration_content"
                    ],
                    "compliance_requirements": ["GDPR"],
                    "data_retention_period": "24 months",
                    "encryption_status": "encrypted_in_transit"
                }
            ],
            "compliance_history": [
                {
                    "assessment_date": "2024-01-15",
                    "overall_score": 82,
                    "assessor": "Internal Audit Team",
                    "key_findings": [
                        "Data retention policies need updating",
                        "Employee training completion below target",
                        "Vendor risk assessments pending"
                    ]
                },
                {
                    "assessment_date": "2023-07-20", 
                    "overall_score": 78,
                    "assessor": "External Auditor",
                    "key_findings": [
                        "GDPR consent mechanisms inadequate",
                        "Incident response plan needs testing",
                        "Access control reviews overdue"
                    ]
                }
            ],
            "recent_incidents": [
                {
                    "date": "2024-02-10",
                    "type": "data_breach",
                    "severity": "medium",
                    "description": "Unauthorized access to development database",
                    "resolution": "Access revoked, additional monitoring implemented"
                }
            ]
        }
    
    @staticmethod
    def get_industry_specific_data(industry: str) -> Dict[str, Any]:
        """Get industry-specific sample data"""
        industry_templates = {
            "healthcare": {
                "company_name": "Sample Healthcare Provider",
                "industry": "healthcare",
                "special_compliance": ["HIPAA", "HITECH", "GDPR"],
                "data_types": ["patient_health_information", "medical_records", "billing_data"],
                "special_considerations": [
                    "PHI protection requirements",
                    "Breach notification timelines",
                    "Business associate agreements"
                ]
            },
            "finance": {
                "company_name": "Sample Financial Institution", 
                "industry": "finance",
                "special_compliance": ["SOX", "GLBA", "PCI-DSS", "GDPR"],
                "data_types": ["financial_transactions", "customer_financial_data", "kyc_documents"],
                "special_considerations": [
                    "Financial reporting controls",
                    "Customer data protection",
                    "Transaction monitoring"
                ]
            },
            "technology": {
                "company_name": "Sample Tech Company",
                "industry": "technology", 
                "special_compliance": ["GDPR", "CCPA", "SOX"],
                "data_types": ["user_data", "intellectual_property", "system_logs"],
                "special_considerations": [
                    "Global data transfer mechanisms",
                    "Open source compliance",
                    "Cloud security configurations"
                ]
            }
        }
        
        base_data = SampleData.get_sample_company_data()
        industry_data = industry_templates.get(industry, industry_templates["technology"])
        
        return {**base_data, **industry_data}
    
    @staticmethod
    def get_compliance_test_cases() -> List[Dict[str, Any]]:
        """Get test cases for compliance validation"""
        return [
            {
                "name": "Full Compliance - Mature Organization",
                "description": "Well-established company with comprehensive compliance program",
                "expected_score_range": (85, 95),
                "characteristics": [
                    "Comprehensive policies and procedures",
                    "Regular employee training",
                    "Documented incident response",
                    "Third-party risk management",
                    "Continuous monitoring"
                ]
            },
            {
                "name": "Partial Compliance - Growing Company", 
                "description": "Mid-sized company with basic compliance framework",
                "expected_score_range": (65, 80),
                "characteristics": [
                    "Basic policies in place",
                    "Limited training programs", 
                    "Ad-hoc incident response",
                    "Minimal third-party oversight",
                    "Periodic assessments"
                ]
            },
            {
                "name": "Low Compliance - Startup",
                "description": "Early-stage company with minimal compliance infrastructure",
                "expected_score_range": (40, 60),
                "characteristics": [
                    "Limited formal policies",
                    "No structured training",
                    "No incident response plan",
                    "No vendor assessments",
                    "Reactive approach to compliance"
                ]
            },
            {
                "name": "High Risk - Healthcare Provider",
                "description": "Organization handling sensitive health data",
                "expected_score_range": (70, 90),
                "characteristics": [
                    "HIPAA compliance requirements",
                    "Strict data access controls",
                    "Regular security assessments",
                    "Comprehensive breach response",
                    "Business associate agreements"
                ]
            }
        ]