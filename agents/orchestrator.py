"""
Compliance Orchestrator - Coordinates multi-agent workflow
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from .monitor_agent import RegulationMonitorAgent
from .analyzer_agent import ComplianceAnalyzerAgent
from .risk_agent import RiskAssessmentAgent
from .reporter_agent import ReportGeneratorAgent

logger = logging.getLogger(__name__)

class ComplianceOrchestrator:
    """Orchestrates the multi-agent compliance workflow"""
    
    def __init__(self, config: Dict, memory_bank, tools: Dict):
        self.config = config
        self.memory_bank = memory_bank
        self.tools = tools
        self.agents = self._initialize_agents()
        self.monitoring_task = None
        self.workflow_history = []
        
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all compliance agents"""
        logger.info("Initializing compliance agents")
        
        agents = {
            'monitor': RegulationMonitorAgent(self.config, self.tools),
            'analyzer': ComplianceAnalyzerAgent(self.config, self.tools),
            'risk_assessor': RiskAssessmentAgent(self.config, self.tools),
            'reporter': ReportGeneratorAgent(self.config, self.tools),
        }
        
        logger.info(f"Initialized {len(agents)} compliance agents")
        return agents
    
    async def execute_compliance_check(self, company_data: Dict) -> Dict:
        """Execute full compliance check workflow"""
        logger.info("Starting compliance check workflow")
        
        workflow_start = datetime.now()
        workflow_id = f"WF-{workflow_start.strftime('%Y%m%d-%H%M%S')}"
        
        try:
            # STEP 1: Parallel data collection
            logger.info("Phase 1: Collecting regulatory and company data")
            monitor_task = asyncio.create_task(
                self.agents['monitor'].gather_regulatory_data()
            )
            analyzer_task = asyncio.create_task(
                self.agents['analyzer'].collect_company_data(company_data)
            )
            
            regulatory_data, enriched_company_data = await asyncio.gather(
                monitor_task, analyzer_task
            )
            
            logger.info(f"Collected data for {len(regulatory_data.get('regulatory_data', {}))} regulations")
            
            # STEP 2: Sequential analysis pipeline
            logger.info("Phase 2: Analyzing compliance")
            analysis_results = await self.agents['analyzer'].analyze_compliance(
                enriched_company_data, regulatory_data
            )
            
            logger.info(f"Compliance analysis completed. Score: {analysis_results.get('overall_score', 0)}%")
            
            risk_assessment = await self.agents['risk_assessor'].assess_risk(
                analysis_results
            )
            
            logger.info(f"Risk assessment completed. Risk score: {risk_assessment.get('overall_risk_score', 0)}")
            
            # STEP 3: Generate comprehensive report
            logger.info("Phase 3: Generating compliance report")
            final_report = await self.agents['reporter'].generate_report(
                analysis_results, risk_assessment
            )
            
            # STEP 4: Store in memory bank
            if self.memory_bank:
                await self.memory_bank.store_compliance_check(
                    company_data.get('company_id', 'unknown'),
                    final_report
                )
            
            # Record workflow completion
            workflow_duration = (datetime.now() - workflow_start).total_seconds()
            
            workflow_record = {
                "workflow_id": workflow_id,
                "company_id": company_data.get('company_id', 'unknown'),
                "duration_seconds": workflow_duration,
                "final_score": analysis_results.get('overall_score', 0),
                "risk_score": risk_assessment.get('overall_risk_score', 0),
                "timestamp": workflow_start.isoformat(),
                "status": "completed"
            }
            
            self.workflow_history.append(workflow_record)
            
            logger.info(f"Compliance check completed in {workflow_duration:.2f}s. Overall score: {final_report['executive_summary']['overall_compliance_score']}%")
            
            return {
                "workflow_id": workflow_id,
                "report": final_report,
                "analysis": analysis_results,
                "risk_assessment": risk_assessment,
                "workflow_metrics": workflow_record
            }
            
        except Exception as e:
            logger.error(f"Compliance workflow failed: {e}")
            
            workflow_record = {
                "workflow_id": workflow_id,
                "company_id": company_data.get('company_id', 'unknown'),
                "duration_seconds": (datetime.now() - workflow_start).total_seconds(),
                "error": str(e),
                "timestamp": workflow_start.isoformat(),
                "status": "failed"
            }
            
            self.workflow_history.append(workflow_record)
            raise
    
    async def start_continuous_monitoring(self):
        """Start continuous compliance monitoring loop"""
        logger.info("Starting continuous compliance monitoring")
        
        async def monitoring_loop():
            while True:
                try:
                    # Check for regulatory changes
                    changes = await self.agents['monitor'].detect_regulatory_changes()
                    
                    if changes and changes.get('has_changes', False):
                        logger.info(f"Detected {len(changes.get('changes', []))} regulatory changes")
                        
                        # In production, this would trigger re-analysis for affected companies
                        for change in changes.get('changes', []):
                            logger.info(f"Regulatory change: {change.get('regulation')} - {change.get('description')}")
                        
                        # Example: You could integrate with a company database here
                        # affected_companies = await self.get_affected_companies(changes)
                        # reanalysis_tasks = [self.execute_compliance_check(company) for company in affected_companies]
                        # await asyncio.gather(*reanalysis_tasks)
                    
                    # Wait for next check interval
                    polling_interval = self.config['agents']['regulation_monitor'].get('polling_interval', 3600)
                    await asyncio.sleep(polling_interval)
                    
                except asyncio.CancelledError:
                    logger.info("Monitoring loop cancelled")
                    break
                except Exception as e:
                    logger.error(f"Monitoring loop error: {e}")
                    await asyncio.sleep(300)  # Wait 5 minutes before retry
        
        self.monitoring_task = asyncio.create_task(monitoring_loop())
    
    async def get_workflow_history(self) -> List[Dict]:
        """Get workflow execution history"""
        return self.workflow_history.copy()
    
    async def get_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics from all agents"""
        metrics = {}
        for agent_name, agent in self.agents.items():
            metrics[agent_name] = agent.get_metrics()
        return metrics
    
    async def shutdown(self):
        """Graceful shutdown of all agents"""
        logger.info("Shutting down orchestrator and agents")
        
        # Cancel monitoring task
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        # Shutdown all agents
        shutdown_tasks = []
        for agent_name, agent in self.agents.items():
            shutdown_tasks.append(agent.shutdown())
        
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        logger.info("All agents shut down successfully")