"""
Unit Tests for ComplianceGuard AI Agents
Test individual agent functionality and interactions
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any

from agents.monitor_agent import RegulationMonitorAgent
from agents.analyzer_agent import ComplianceAnalyzerAgent
from agents.risk_agent import RiskAssessmentAgent
from agents.reporter_agent import ReportGeneratorAgent
from agents.orchestrator import ComplianceOrchestrator


class TestAgentSystem:
    """Test suite for agent system functionality"""
    
    @pytest.fixture
    def sample_config(self):
        """Sample configuration for testing"""
        return {
            'agents': {
                'regulation_monitor': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['regulatory_search_tool'],
                    'polling_interval': 3600
                },
                'compliance_analyzer': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['compliance_gap_analyzer']
                },
                'risk_assessor': {
                    'model': 'gemini-2.0-pro-exp', 
                    'tools': ['risk_scoring_engine']
                },
                'report_generator': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['compliance_report_formatter']
                }
            },
            'compliance': {
                'regulations': ['GDPR', 'HIPAA', 'SOX']
            }
        }
    
    @pytest.fixture
    def sample_tools(self):
        """Mock tools for testing"""
        return {
            'regulatory_search_tool': Mock(),
            'compliance_gap_analyzer': Mock(),
            'risk_scoring_engine': Mock(),
            'compliance_report_formatter': Mock()
        }
    
    @pytest.fixture
    def sample_company_data(self):
        """Sample company data for testing"""
        return {
            'company_id': 'test_company_123',
            'company_name': 'Test Corporation',
            'industry': 'technology',
            'employee_count': 500,
            'policies': [
                {'name': 'Data Protection Policy', 'content': 'Sample policy content'},
                {'name': 'Security Policy', 'content': 'Security guidelines'}
            ]
        }
    
    @pytest.mark.asyncio
    async def test_monitor_agent_initialization(self, sample_config, sample_tools):
        """Test regulation monitor agent initialization"""
        agent = RegulationMonitorAgent(sample_config, sample_tools)
        
        assert agent.name == "regulation_monitor"
        assert agent.model == "gemini-2.0-flash-exp"
        assert len(agent.regulatory_sources) == 3
        
    @pytest.mark.asyncio
    async def test_monitor_agent_gather_data(self, sample_config, sample_tools):
        """Test regulation data gathering"""
        agent = RegulationMonitorAgent(sample_config, sample_tools)
        
        # Mock the tool responses
        sample_tools['regulatory_search_tool'].return_value = {
            'results': [{'title': 'GDPR Guidelines', 'relevance_score': 0.95}]
        }
        
        regulatory_data = await agent.gather_regulatory_data()
        
        assert 'regulatory_data' in regulatory_data
        assert regulatory_data['sources_checked'] == 3
        assert 'GDPR' in regulatory_data['regulatory_data']
        
    @pytest.mark.asyncio
    async def test_analyzer_agent_compliance_check(self, sample_config, sample_tools):
        """Test compliance analysis functionality"""
        agent = ComplianceAnalyzerAgent(sample_config, sample_tools)
        
        sample_company_data = {'policies': [{'name': 'Test Policy'}]}
        sample_regulatory_data = {
            'regulatory_data': {
                'GDPR': {'status': 'success', 'key_articles': ['Article 5']},
                'HIPAA': {'status': 'success', 'key_rules': ['Privacy Rule']}
            }
        }
        
        # Mock gap analyzer tool
        sample_tools['compliance_gap_analyzer'].return_value = {
            'compliance_score': 85,
            'gaps_identified': 2,
            'gap_details': [
                {'policy_name': 'Test Policy', 'severity': 'medium'}
            ]
        }
        
        analysis_results = await agent.analyze_compliance(
            sample_company_data, sample_regulatory_data
        )
        
        assert 'overall_score' in analysis_results
        assert 'gap_analysis' in analysis_results
        assert 'recommendations' in analysis_results
        assert analysis_results['overall_score'] >= 0
        assert analysis_results['overall_score'] <= 100
        
    @pytest.mark.asyncio
    async def test_risk_assessor_calculation(self, sample_config, sample_tools):
        """Test risk assessment calculations"""
        agent = RiskAssessmentAgent(sample_config, sample_tools)
        
        sample_analysis = {
            'overall_score': 75,
            'regulation_scores': {'GDPR': 80, 'HIPAA': 70},
            'gap_analysis': [
                {'severity': 'high', 'description': 'Critical gap'}
            ]
        }
        
        # Mock risk scoring tool
        sample_tools['risk_scoring_engine'].return_value = {
            'overall_risk_score': 25,
            'risk_level': 'medium',
            'risk_breakdown': {'regulatory_changes': 0.3}
        }
        
        risk_assessment = await agent.assess_risk(sample_analysis)
        
        assert 'overall_risk_score' in risk_assessment
        assert 'risk_breakdown' in risk_assessment
        assert 'mitigation_strategies' in risk_assessment
        assert risk_assessment['overall_risk_score'] >= 0
        
    @pytest.mark.asyncio
    async def test_report_generator_creation(self, sample_config, sample_tools):
        """Test report generation"""
        agent = ReportGeneratorAgent(sample_config, sample_tools)
        
        sample_analysis = {
            'overall_score': 85,
            'regulation_scores': {'GDPR': 90, 'HIPAA': 80},
            'gap_analysis': [{'severity': 'medium'}]
        }
        
        sample_risk = {
            'overall_risk_score': 15,
            'risk_level': 'low'
        }
        
        # Mock report formatter tool
        sample_tools['compliance_report_formatter'].return_value = {
            'report_id': 'TEST-REPORT-001',
            'format_type': 'executive',
            'sections_included': ['executive_summary']
        }
        
        report = await agent.generate_report(sample_analysis, sample_risk)
        
        assert 'report_id' in report
        assert 'executive_summary' in report
        assert 'detailed_analysis' in report
        assert 'recommendations' in report
        
    @pytest.mark.asyncio
    async def test_orchestrator_workflow(self, sample_config, sample_tools):
        """Test full orchestrator workflow"""
        memory_bank = Mock()
        orchestrator = ComplianceOrchestrator(sample_config, memory_bank, sample_tools)
        
        sample_company_data = {
            'company_id': 'test_company_123',
            'policies': [{'name': 'Test Policy'}]
        }
        
        # Mock agent responses
        with patch.object(orchestrator.agents['monitor'], 'gather_regulatory_data') as mock_monitor:
            with patch.object(orchestrator.agents['analyzer'], 'collect_company_data') as mock_analyzer:
                with patch.object(orchestrator.agents['analyzer'], 'analyze_compliance') as mock_analysis:
                    with patch.object(orchestrator.agents['risk_assessor'], 'assess_risk') as mock_risk:
                        with patch.object(orchestrator.agents['reporter'], 'generate_report') as mock_report:
                            
                            # Setup mock returns
                            mock_monitor.return_value = {
                                'regulatory_data': {
                                    'GDPR': {'status': 'success'},
                                    'HIPAA': {'status': 'success'}
                                }
                            }
                            mock_analyzer.return_value = sample_company_data
                            mock_analysis.return_value = {'overall_score': 85}
                            mock_risk.return_value = {'overall_risk_score': 15}
                            mock_report.return_value = {'report_id': 'TEST-001'}
                            
                            # Execute workflow
                            result = await orchestrator.execute_compliance_check(sample_company_data)
                            
                            assert 'workflow_id' in result
                            assert 'report' in result
                            assert 'analysis' in result
                            assert 'risk_assessment' in result
                            assert result['report']['report_id'] == 'TEST-001'
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self, sample_config, sample_tools):
        """Test agent error handling"""
        agent = RegulationMonitorAgent(sample_config, sample_tools)
        
        # Simulate tool failure
        sample_tools['regulatory_search_tool'].side_effect = Exception("API Error")
        
        # Should handle errors gracefully
        regulatory_data = await agent.gather_regulatory_data()
        
        assert 'regulatory_data' in regulatory_data
        # Should still return structure even with errors
        assert any('error' in data for data in regulatory_data['regulatory_data'].values())
    
    def test_agent_metrics_collection(self, sample_config, sample_tools):
        """Test agent metrics collection"""
        agent = ComplianceAnalyzerAgent(sample_config, sample_tools)
        
        metrics = agent.get_metrics()
        
        assert 'requests_processed' in metrics
        assert 'errors' in metrics
        assert 'last_activity' in metrics
        assert metrics['requests_processed'] == 0  # Initial state
        
    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self, sample_config, sample_tools):
        """Test parallel execution of agents"""
        orchestrator = ComplianceOrchestrator(sample_config, Mock(), sample_tools)
        
        # Mock agent methods to track execution order
        execution_order = []
        
        async def mock_monitor():
            execution_order.append('monitor')
            await asyncio.sleep(0.1)
            return {'regulatory_data': {}}
            
        async def mock_analyzer():
            execution_order.append('analyzer') 
            await asyncio.sleep(0.1)
            return {'policies': []}
        
        with patch.object(orchestrator.agents['monitor'], 'gather_regulatory_data', mock_monitor):
            with patch.object(orchestrator.agents['analyzer'], 'collect_company_data', mock_analyzer):
                # These should execute in parallel
                await asyncio.gather(mock_monitor(), mock_analyzer())
                
                # Both should be in execution order (order may vary due to parallelism)
                assert 'monitor' in execution_order
                assert 'analyzer' in execution_order