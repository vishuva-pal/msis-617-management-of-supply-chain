"""
Performance Tests for ComplianceGuard AI
Test system performance, scalability, and resource usage
"""

import pytest
import asyncio
import time
import psutil
import os
from typing import Dict, Any, List

from main import ComplianceGuardAI
from agents.orchestrator import ComplianceOrchestrator
from memory.memory_bank import ComplianceMemoryBank
from tools.setup_tools import initialize_tools


class TestPerformance:
    """Performance test suite for ComplianceGuard AI"""
    
    @pytest.fixture
    def performance_config(self):
        """Configuration optimized for performance testing"""
        return {
            'agents': {
                'regulation_monitor': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['regulation_database_tool'],  # Minimal tools for perf
                    'polling_interval': 3600
                },
                'compliance_analyzer': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['compliance_gap_analyzer']
                },
                'risk_assessor': {
                    'model': 'gemini-2.0-flash-exp',  # Use flash for perf
                    'tools': ['risk_scoring_engine']
                },
                'report_generator': {
                    'model': 'gemini-2.0-flash-exp',
                    'tools': ['compliance_report_formatter']
                }
            },
            'compliance': {
                'regulations': ['GDPR', 'HIPAA']  # Reduced set for perf
            }
        }
    
    @pytest.fixture
    def sample_company_data(self):
        """Optimized company data for performance testing"""
        return {
            'company_id': 'perf_test_company',
            'company_name': 'Performance Test Corp',
            'policies': [
                {
                    'name': 'Data Policy',
                    'content': 'Basic data protection policy content for testing.'
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_single_compliance_check_performance(self, performance_config, sample_company_data):
        """Test performance of single compliance check"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(performance_config)
        orchestrator = ComplianceOrchestrator(performance_config, memory_bank, tools)
        
        # Measure execution time
        start_time = time.time()
        
        result = await orchestrator.execute_compliance_check(sample_company_data)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Performance assertions
        assert execution_time < 5.0  # Should complete within 5 seconds
        assert result['workflow_metrics']['status'] == 'completed'
        
        # Verify result quality
        assert result['analysis']['overall_score'] >= 0
        assert result['analysis']['overall_score'] <= 100
        
        await orchestrator.shutdown()
    
    @pytest.mark.asyncio
    async def test_concurrent_compliance_checks(self, performance_config):
        """Test performance under concurrent load"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(performance_config)
        orchestrator = ComplianceOrchestrator(performance_config, memory_bank, tools)
        
        async def run_check(company_id):
            company_data = {
                'company_id': company_id,
                'company_name': f'Company {company_id}',
                'policies': [{'name': 'Policy', 'content': 'Content'}]
            }
            return await orchestrator.execute_compliance_check(company_data)
        
        # Test different concurrency levels
        concurrency_levels = [1, 3, 5]
        
        for concurrency in concurrency_levels:
            start_time = time.time()
            
            tasks = [run_check(f'company_{i}') for i in range(concurrency)]
            results = await asyncio.gather(*tasks)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # All tasks should complete successfully
            assert len(results) == concurrency
            assert all(r['workflow_metrics']['status'] == 'completed' for r in results)
            
            print(f"Concurrency {concurrency}: {total_time:.2f}s total, {total_time/concurrency:.2f}s per check")
            
            # Throughput should be reasonable
            assert total_time < 10 * concurrency  # Linear scaling expectation
        
        await orchestrator.shutdown()
    
    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self, performance_config):
        """Test memory usage during operation"""
        process = psutil.Process(os.getpid())
        
        # Measure baseline memory
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(performance_config)
        orchestrator = ComplianceOrchestrator(performance_config, memory_bank, tools)
        
        # Run multiple operations
        for i in range(10):
            company_data = {
                'company_id': f'memory_test_{i}',
                'policies': [{'name': 'Policy', 'content': 'Content' * 100}]  # Larger content
            }
            await orchestrator.execute_compliance_check(company_data)
        
        # Measure memory after operations
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory usage: {initial_memory:.2f}MB -> {final_memory:.2f}MB (+{memory_increase:.2f}MB)")
        
        # Memory increase should be reasonable
        assert memory_increase < 500  # Should not increase by more than 500MB
        
        await orchestrator.shutdown()
    
    @pytest.mark.asyncio
    async def test_response_time_consistency(self, performance_config, sample_company_data):
        """Test that response times remain consistent"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(performance_config)
        orchestrator = ComplianceOrchestrator(performance_config, memory_bank, tools)
        
        response_times = []
        
        # Run multiple iterations
        for i in range(10):
            start_time = time.time()
            
            result = await orchestrator.execute_compliance_check(sample_company_data)
            
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
            
            assert result['workflow_metrics']['status'] == 'completed'
        
        # Calculate statistics
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        variance = max_response_time - min_response_time
        
        print(f"Response times: {min_response_time:.2f}s - {max_response_time:.2f}s (avg: {avg_response_time:.2f}s)")
        
        # Response times should be consistent
        assert variance < 2.0  # Less than 2 seconds variance
        assert avg_response_time < 3.0  # Average under 3 seconds
        
        await orchestrator.shutdown()
    
    @pytest.mark.asyncio
    async def test_memory_bank_scalability(self):
        """Test memory bank performance with large datasets"""
        memory_bank = ComplianceMemoryBank(max_entries=10000)
        
        # Store large number of entries
        start_time = time.time()
        
        for i in range(1000):
            company_data = {
                'executive_summary': {
                    'overall_compliance_score': i % 100,
                    'overall_risk_score': 100 - (i % 100)
                },
                'detailed_analysis': {
                    'regulation_performance': {'GDPR': i % 100, 'HIPAA': (i + 10) % 100},
                    'gap_breakdown': {
                        'GDPR': [{'severity': 'high', 'description': f'Gap {i}'}]
                    }
                }
            }
            
            await memory_bank.store_compliance_check(f'company_{i % 100}', company_data)
        
        storage_time = time.time() - start_time
        
        # Storage should be efficient
        assert storage_time < 10.0  # 1000 entries in under 10 seconds
        
        # Test retrieval performance
        start_time = time.time()
        
        for i in range(100):
            history = await memory_bank.retrieve_compliance_history(f'company_{i}')
            assert len(history) > 0
        
        retrieval_time = time.time() - start_time
        
        # Retrieval should be fast
        assert retrieval_time < 5.0  # 100 retrievals in under 5 seconds
        
        # Test trend analysis performance
        start_time = time.time()
        
        trends = await memory_bank.get_compliance_trends('company_0')
        assert 'score_trend' in trends
        
        analysis_time = time.time() - start_time
        
        # Analysis should be efficient
        assert analysis_time < 2.0
        
        print(f"Storage: {storage_time:.2f}s, Retrieval: {retrieval_time:.2f}s, Analysis: {analysis_time:.2f}s")
    
    @pytest.mark.asyncio
    async def test_agent_initialization_performance(self, performance_config):
        """Test agent initialization performance"""
        start_time = time.time()
        
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(performance_config)
        orchestrator = ComplianceOrchestrator(performance_config, memory_bank, tools)
        
        initialization_time = time.time() - start_time
        
        # System should initialize quickly
        assert initialization_time < 5.0
        
        await orchestrator.shutdown()
    
    def test_system_resource_limits(self):
        """Test that system operates within resource limits"""
        process = psutil.Process(os.getpid())
        
        # Check current resource usage
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()
        
        print(f"Current resources - Memory: {memory_mb:.2f}MB, CPU: {cpu_percent:.1f}%")
        
        # System should not be using excessive resources at idle
        assert memory_mb < 1000  # Under 1GB at idle
        assert cpu_percent < 50  # Under 50% CPU at idle
    
    @pytest.mark.asyncio
    async def test_error_handling_performance(self, performance_config, sample_company_data):
        """Test that error handling doesn't significantly impact performance"""
        memory_bank = ComplianceMemoryBank()
        tools = initialize_tools(performance_config)
        orchestrator = ComplianceOrchestrator(performance_config, memory_bank, tools)
        
        # Time normal operation
        start_time = time.time()
        normal_result = await orchestrator.execute_compliance_check(sample_company_data)
        normal_time = time.time() - start_time
        
        # Time operation with simulated error
        with patch.object(orchestrator.agents['monitor'], 'gather_regulatory_data') as mock_monitor:
            mock_monitor.side_effect = Exception("Simulated error")
            
            start_time = time.time()
            try:
                error_result = await orchestrator.execute_compliance_check(sample_company_data)
                error_time = time.time() - start_time
            except Exception:
                error_time = time.time() - start_time
        
        # Error handling should not be significantly slower
        time_difference = abs(error_time - normal_time)
        assert time_difference < 2.0  # Within 2 seconds difference
        
        print(f"Normal: {normal_time:.2f}s, Error: {error_time:.2f}s, Difference: {time_difference:.2f}s")
        
        await orchestrator.shutdown()