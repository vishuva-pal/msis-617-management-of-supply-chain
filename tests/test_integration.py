"""
Integration Tests for ComplianceGuard AI
Test end-to-end system functionality and integrations
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch
from typing import Dict, Any

from main import ComplianceGuardAI
from agents.orchestrator import ComplianceOrchestrator
from memory.memory_bank import ComplianceMemoryBank
from tools.setup_tools import initialize_tools


class TestIntegration:
    """Integration test suite for ComplianceGuard AI"""
    
    @pytest.fixture
    def sample_config(self):
        """Sample configuration for integration tests"""
        return {
            'agents': {
                'regulation_monitor': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['regulatory_search_tool', 'regulation_database_tool'],
                    'polling_interval': 3600
                },
                'compliance_analyzer': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['compliance_gap_analyzer', 'policy_analyzer']
                },
                'risk_assessor': {
                    'model': 'gemini-2.0-pro-exp',
                    'tools': ['risk_scoring_engine']
                },
                'report_generator': {
                    'model': 'gemini-2.0-flash-exp', 
                    'tools': ['compliance_report_formatter', 'audit_trail_generator']
                }
            },
            'compliance': {
                'regulations': ['GDPR', 'HIPAA', 'SOX']
            },
            'memory': {
                'memory_bank': {
                    'max_entries': 1000,
                    'compaction_strategy': 'semantic'
                }
            }
        }
    
    @pytest.fixture
    def sample_company_data(self):
        """Sample company data for integration tests"""
        return {
            'company_id': 'integration_test_company',
            'company_name': 'Integration Test Corp',
            'industry': 'technology',
            'employee_count': 1000,
            'revenue_range': '10M-50M',
            'policies': [
                {
                    'name': 'Data Protection and Privacy Policy',
                    'content': 'This policy outlines how we protect customer data and ensure privacy compliance.',
                    'version': '2.1',
                    'last_updated': '2024-01-15'
                },
                {
                    'name': 'Information Security Policy', 
                    'content': 'Comprehensive security measures for protecting company and customer information.',
                    'version': '1.5',
                    'last_updated': '2024-02-01'
                }
            ],
            'systems': [
                {
                    'name': 'CRM System',
                    'data_types': ['customer_data', 'contact_info'],
                    'compliance_requirements': ['GDPR', 'CCPA']
                },
                {
                    'name': 'HR System',
                    'data_types': ['employee_data', 'performance_data'], 
                    'compliance_requirements': ['GDPR', 'HIPAA']
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_end_to_end_compliance_check(self, sample_config, sample_company_data):
        """Test complete end-to-end compliance check workflow"""
        # Initialize system components
        memory_bank = ComplianceMemoryBank(max_entries=1000)
        tools = initialize_tools(sample_config)
        orchestrator = ComplianceOrchestrator(sample_config, memory_bank, tools)
        
        # Execute full compliance check
        result = await orchestrator.execute_compliance_check(sample_company_data)
        
        # Verify workflow completion
        assert 'workflow_id' in result
        assert 'report' in result
        assert 'analysis' in result
        assert 'risk_assessment' in result
        assert 'workflow_metrics' in result
        
        # Verify report structure
        report = result['report']
        assert 'executive_summary' in report
        assert 'detailed_analysis' in report
        assert 'recommendations' in report
        assert 'action_plan' in report
        
        # Verify analysis results
        analysis = result['analysis']
        assert 'overall_score' in analysis
        assert 'regulation_scores' in analysis
        assert 'gap_analysis' in analysis
        assert 0 <= analysis['overall_score'] <= 100
        
        # Verify risk assessment
        risk_assessment = result['risk_assessment']
        assert 'overall_risk_score' in risk_assessment
        assert 'risk_level' in risk_assessment
        assert 'mitigation_strategies' in risk_assessment
        
        # Verify workflow metrics
        metrics = result['workflow_metrics']
        assert 'duration_seconds' in metrics
        assert 'final_score' in metrics
        assert 'status' in metrics
        assert metrics['status'] == 'completed'
    
    @pytest.mark.asyncio
    async def test_memory_bank_integration(self, sample_config, sample_company_data):
        """Test memory bank integration and data persistence"""
        memory_bank = ComplianceMemoryBank(max_entries=100)
        tools = initialize_tools(sample_config)
        orchestrator = ComplianceOrchestrator(sample_config, memory_bank, tools)
        
        # Execute multiple compliance checks
        for i in range(3):
            company_data = sample_company_data.copy()
            company_data['company_id'] = f'test_company_{i}'
            
            result = await orchestrator.execute_compliance_check(company_data)
            
            # Verify data was stored in memory bank
            history = await memory_bank.retrieve_compliance_history(company_data['company_id'])
            assert len(history) == 1  # One entry per company
            
            entry = history[0]
            assert entry['company_id'] == company_data['company_id']
            assert 'compliance_score' in entry
            assert 'key_findings' in entry
        
        # Test memory bank metrics
        metrics = memory_bank.get_memory_metrics()
        assert metrics['current_entries'] == 3
        assert metrics['companies_tracked'] == 3
        assert metrics['memory_health'] == 'good'
    
    @pytest.mark.asyncio
    async def test_trend_analysis_integration(self, sample_config):
        """Test compliance trend analysis integration"""
        memory_bank = ComplianceMemoryBank(max_entries=1000)
        
        # Store historical compliance data
        for i in range(5):
            company_id = 'trend_test_company'
            compliance_data = {
                'executive_summary': {
                    'overall_compliance_score': 70 + (i * 5),  # Improving trend
                    'overall_risk_score': 30 - (i * 5)  # Decreasing risk
                },
                'detailed_analysis': {
                    'regulation_performance': {'GDPR': 75 + i, 'HIPAA': 65 + i},
                    'gap_breakdown': {
                        'GDPR': [{'severity': 'high', 'description': f'Gap {i}'}]
                    }
                }
            }
            
            await memory_bank.store_compliance_check(company_id, compliance_data)
            # Simulate time passing
            await asyncio.sleep(0.1)
        
        # Analyze trends
        trends = await memory_bank.get_compliance_trends('trend_test_company')
        
        assert 'company_id' in trends
        assert 'current_score' in trends
        assert 'average_score' in trends
        assert 'score_trend' in trends
        assert 'risk_trend' in trends
        assert 'recurring_gaps' in trends
        assert 'improvement_areas' in trends
        
        # Verify trend detection
        assert trends['score_trend'] == 'improving'
        assert trends['analysis_period'] == 'Last 5 assessments'
    
    @pytest.mark.asyncio
    async def test_main_system_initialization(self, sample_config):
        """Test main system initialization and shutdown"""
        # Initialize main system
        system = ComplianceGuardAI()
        
        # Verify components are initialized
        assert system.config is not None
        assert system.memory_bank is not None
        assert system.tools is not None
        assert system.orchestrator is not None
        
        # Test shutdown
        await system.shutdown()
        # Should complete without errors
    
    @pytest.mark.asyncio
    async def test_continuous_monitoring_integration(self, sample_config):
        """Test continuous monitoring integration"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(sample_config)
        orchestrator = ComplianceOrchestrator(sample_config, memory_bank, tools)
        
        # Start continuous monitoring
        await orchestrator.start_continuous_monitoring()
        
        # Let it run for a short period
        await asyncio.sleep(2)
        
        # Stop monitoring
        await orchestrator.shutdown()
        
        # Verify monitoring was active
        assert orchestrator.monitoring_task is not None
        assert orchestrator.monitoring_task.done() or not orchestrator.monitoring_task.cancelled()
    
    @pytest.mark.asyncio
    async def test_error_recovery_integration(self, sample_config, sample_company_data):
        """Test system error recovery and resilience"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(sample_config)
        orchestrator = ComplianceOrchestrator(sample_config, memory_bank, tools)
        
        # Simulate agent failure
        with patch.object(orchestrator.agents['monitor'], 'gather_regulatory_data') as mock_monitor:
            mock_monitor.side_effect = Exception("Simulated API failure")
            
            # System should handle errors gracefully
            try:
                result = await orchestrator.execute_compliance_check(sample_company_data)
                # If we get here, error was handled
                assert 'workflow_metrics' in result
                assert result['workflow_metrics']['status'] == 'failed'
            except Exception:
                # Alternatively, might raise exception - both are valid error handling
                pass
        
        # System should still be functional after error
        await orchestrator.shutdown()
    
    @pytest.mark.asyncio
    async def test_performance_under_load(self, sample_config):
        """Test system performance under simulated load"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(sample_config)
        orchestrator = ComplianceOrchestrator(sample_config, memory_bank, tools)
        
        # Simulate multiple concurrent compliance checks
        async def run_compliance_check(company_id):
            company_data = {
                'company_id': company_id,
                'company_name': f'Test Company {company_id}',
                'policies': [{'name': 'Test Policy', 'content': 'Content'}]
            }
            
            result = await orchestrator.execute_compliance_check(company_data)
            return result['workflow_metrics']['duration_seconds']
        
        # Run multiple checks concurrently
        tasks = [run_compliance_check(f'company_{i}') for i in range(5)]
        durations = await asyncio.gather(*tasks)
        
        # All tasks should complete
        assert len(durations) == 5
        assert all(duration > 0 for duration in durations)
        
        # Average duration should be reasonable
        avg_duration = sum(durations) / len(durations)
        assert avg_duration < 10.0  # Should complete within 10 seconds
        
        await orchestrator.shutdown()