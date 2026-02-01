#!/usr/bin/env python3
"""
ComplianceGuard AI - Main Entry Point
Multi-agent system for enterprise compliance automation
"""

import asyncio
import logging
from typing import Dict, Any
import yaml

from agents.orchestrator import ComplianceOrchestrator
from memory.memory_bank import ComplianceMemoryBank
from tools.setup_tools import initialize_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComplianceGuardAI:
    """Main ComplianceGuard AI system class"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.memory_bank = ComplianceMemoryBank()
        self.tools = initialize_tools(self.config)
        self.orchestrator = ComplianceOrchestrator(self.config, self.memory_bank, self.tools)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise
    
    async def execute_compliance_check(self, company_data: Dict) -> Dict:
        """Execute full compliance check workflow"""
        logger.info("Starting compliance check workflow")
        
        try:
            results = await self.orchestrator.execute_compliance_check(company_data)
            logger.info(f"Compliance check completed. Score: {results.get('overall_score', 0)}%")
            return results
            
        except Exception as e:
            logger.error(f"Compliance check failed: {e}")
            raise
    
    async def start_continuous_monitoring(self):
        """Start continuous compliance monitoring"""
        logger.info("Starting continuous compliance monitoring")
        await self.orchestrator.start_continuous_monitoring()
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down ComplianceGuard AI")
        await self.orchestrator.shutdown()

async def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ComplianceGuard AI - Enterprise Compliance Automation")
    parser.add_argument("--company-data", required=True, help="Path to company data JSON file")
    parser.add_argument("--continuous", action="store_true", help="Enable continuous monitoring")
    
    args = parser.parse_args()
    
    # Initialize system
    compliance_ai = ComplianceGuardAI()
    
    try:
        if args.continuous:
            # Start continuous monitoring
            await compliance_ai.start_continuous_monitoring()
        else:
            # Run single compliance check
            import json
            with open(args.company_data, 'r') as f:
                company_data = json.load(f)
            
            results = await compliance_ai.execute_compliance_check(company_data)
            print(json.dumps(results, indent=2))
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        await compliance_ai.shutdown()

if __name__ == "__main__":
    asyncio.run(main())