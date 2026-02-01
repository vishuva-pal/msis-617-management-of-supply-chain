"""
Unit Tests for ComplianceGuard AI Tools
Test custom tool functionality and integrations
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any

from tools.custom_tools import (
    compliance_gap_analyzer,
    risk_scoring_engine,
    policy_analyzer,
    regulatory_search_tool,
    audit_trail_generator,
    compliance_report_formatter
)

from tools.mcp_tools import (
    regulation_database_tool,
    compliance_framework_tool
)


class TestTools:
    """Test suite for tool functionality"""
    
    @pytest.mark.asyncio
    async def test_compliance_gap_analyzer(self):
        """Test gap analysis tool"""
        sample_policies = [
            {'name': 'Data Policy', 'content': 'We handle data responsibly'},
            {'name': 'Security Policy', 'content': 'Basic security measures'}
        ]
        
        sample_regulations = [
            {'name': 'GDPR', 'requirements': ['data protection', 'consent management']},
            {'name': 'HIPAA', 'requirements': ['phi protection', 'access controls']}
        ]
        
        result = await compliance_gap_analyzer(sample_policies, sample_regulations)
        
        assert 'total_policies_analyzed' in result
        assert 'gaps_identified' in result
        assert 'compliance_score' in result
        assert result['total_policies_analyzed'] == 2
        assert 0 <= result['compliance_score'] <= 100
        
    @pytest.mark.asyncio
    async def test_risk_scoring_engine(self):
        """Test risk scoring tool"""
        sample_compliance_data = {
            'gap_analysis': [
                {'severity': 'high', 'description': 'Critical gap'},
                {'severity': 'medium', 'description': 'Moderate gap'}
            ],
            'regulation_scores': {'GDPR': 80, 'HIPAA': 70}
        }
        
        sample_historical_data = {
            'previous_scores': [75, 80, 78],
            'audit_findings': ['minor', 'moderate']
        }
        
        result = await risk_scoring_engine(sample_compliance_data, sample_historical_data)
        
        assert 'overall_risk_score' in result
        assert 'risk_level' in result
        assert 'risk_breakdown' in result
        assert 0 <= result['overall_risk_score'] <= 100
        assert result['risk_level'] in ['low', 'medium', 'high', 'critical']
        
    @pytest.mark.asyncio
    async def test_policy_analyzer(self):
        """Test policy analysis tool"""
        sample_policy_text = """
        This policy outlines our approach to data protection and privacy.
        We comply with relevant regulations and implement appropriate safeguards.
        """
        
        sample_requirements = [
            'Data minimization principle',
            'Purpose limitation', 
            'Storage limitation',
            'Integrity and confidentiality'
        ]
        
        result = await policy_analyzer(sample_policy_text, sample_requirements)
        
        assert 'policy_metrics' in result
        assert 'requirements_covered' in result
        assert 'coverage_percentage' in result
        assert 'missing_requirements' in result
        assert 0 <= result['coverage_percentage'] <= 100
        
    @pytest.mark.asyncio
    async def test_regulatory_search_tool(self):
        """Test regulatory search tool"""
        sample_query = "data retention requirements"
        sample_jurisdictions = ["EU", "US", "Global"]
        
        result = await regulatory_search_tool(sample_query, sample_jurisdictions)
        
        assert 'query' in result
        assert 'jurisdictions_searched' in result
        assert 'total_results' in result
        assert 'results' in result
        assert result['query'] == sample_query
        assert len(result['results']) <= 5  # Should return top 5 results
        
    @pytest.mark.asyncio
    async def test_audit_trail_generator(self):
        """Test audit trail generation"""
        sample_actions = [
            {'type': 'policy_update', 'description': 'Updated data protection policy'},
            {'type': 'compliance_check', 'description': 'Monthly compliance assessment'},
            {'type': 'training_completion', 'description': 'Employee privacy training'}
        ]
        
        result = await audit_trail_generator(sample_actions, timeframe_days=30)
        
        assert 'audit_trail_id' in result
        assert 'total_events' in result
        assert 'events' in result
        assert result['total_events'] == len(sample_actions)
        assert len(result['events']) == len(sample_actions)
        
    @pytest.mark.asyncio
    async def test_compliance_report_formatter(self):
        """Test report formatting tool"""
        sample_report_data = {
            'report_id': 'TEST-REPORT-001',
            'executive_summary': {
                'overall_compliance_score': 85,
                'compliance_status': 'good'
            },
            'detailed_analysis': {
                'regulation_performance': {'GDPR': 90, 'HIPAA': 80}
            }
        }
        
        format_types = ['executive', 'detailed', 'technical', 'regulatory']
        
        for format_type in format_types:
            result = await compliance_report_formatter(sample_report_data, format_type)
            
            assert 'report_id' in result
            assert 'format_type' in result
            assert 'sections_included' in result
            assert result['format_type'] == format_type
            assert len(result['sections_included']) > 0
            
    @pytest.mark.asyncio
    async def test_regulation_database_tool(self):
        """Test regulation database access"""
        regulations = ['GDPR', 'HIPAA', 'SOX', 'UNKNOWN_REGULATION']
        
        for regulation in regulations:
            result = await regulation_database_tool(regulation)
            
            assert 'query_timestamp' in result
            
            if regulation != 'UNKNOWN_REGULATION':
                assert 'full_name' in result
                assert 'jurisdiction' in result
                assert 'key_requirements' in result
            else:
                assert 'error' in result
                assert 'available_regulations' in result
                
    @pytest.mark.asyncio
    async def test_compliance_framework_tool(self):
        """Test compliance framework access"""
        frameworks = ['NIST_CSF', 'ISO_27001', 'COBIT', 'UNKNOWN_FRAMEWORK']
        
        for framework in frameworks:
            result = await compliance_framework_tool(framework, 'technology')
            
            assert 'query_timestamp' in result
            
            if framework != 'UNKNOWN_FRAMEWORK':
                assert 'full_name' in result
                assert 'version' in result
                assert 'domains' in result
            else:
                assert 'error' in result
                assert 'available_frameworks' in result
                
    @pytest.mark.asyncio
    async def test_tool_error_handling(self):
        """Test tool error handling"""
        # Test with invalid inputs
        result = await compliance_gap_analyzer([], [])
        
        # Should handle empty inputs gracefully
        assert 'total_policies_analyzed' in result
        assert result['total_policies_analyzed'] == 0
        
    @pytest.mark.asyncio 
    async def test_tool_performance(self):
        """Test tool performance characteristics"""
        import time
        
        # Test that tools complete within reasonable time
        start_time = time.time()
        
        result = await compliance_gap_analyzer(
            [{'name': 'Test Policy', 'content': 'Content'}],
            [{'name': 'Test Regulation', 'requirements': ['req1', 'req2']}]
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within 2 seconds
        assert execution_time < 2.0
        assert 'compliance_score' in result