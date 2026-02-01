"""
Regulation Monitor Agent - Tracks regulatory changes
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from .base_agent import BaseComplianceAgent

logger = logging.getLogger(__name__)

class RegulationMonitorAgent(BaseComplianceAgent):
    """Monitors regulatory changes across multiple jurisdictions"""
    
    def __init__(self, config: Dict, tools: Dict):
        super().__init__("regulation_monitor", config, tools)
        self.regulatory_sources = config['compliance']['regulations']
        self.last_check = None
        
    async def execute_task(self, task_data: Dict) -> Dict:
        """Execute monitoring task"""
        if task_data.get('type') == 'gather_regulations':
            return await self.gather_regulatory_data()
        elif task_data.get('type') == 'check_changes':
            return await self.detect_regulatory_changes()
        else:
            return await self.gather_regulatory_data()
        
    async def gather_regulatory_data(self) -> Dict[str, Any]:
        """Gather current regulatory requirements"""
        logger.info(f"Gathering regulatory data for {len(self.regulatory_sources)} jurisdictions")
        
        regulatory_data = {}
        
        # Parallel data collection for each regulation
        tasks = []
        for regulation in self.regulatory_sources:
            task = asyncio.create_task(
                self._fetch_regulation_data(regulation)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for regulation, result in zip(self.regulatory_sources, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch {regulation}: {result}")
                regulatory_data[regulation] = {"error": str(result), "status": "failed"}
            else:
                regulatory_data[regulation] = result
                regulatory_data[regulation]["status"] = "success"
        
        self.last_check = datetime.now()
        
        return {
            "regulatory_data": regulatory_data,
            "timestamp": self.last_check.isoformat(),
            "sources_checked": len(self.regulatory_sources),
            "successful_fetches": len([r for r in regulatory_data.values() if r.get('status') == 'success'])
        }
    
    async def _fetch_regulation_data(self, regulation: str) -> Dict[str, Any]:
        """Fetch data for a specific regulation"""
        try:
            # Simulate API call delay
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            regulation_data = {
                "regulation": regulation,
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "source": "ComplianceGuard AI Regulatory Database",
                "version": "2025.1"
            }
            
            # Add regulation-specific content
            if regulation.upper() == "GDPR":
                regulation_data.update({
                    "key_articles": [
                        "Article 5 - Data processing principles",
                        "Article 6 - Lawfulness of processing",
                        "Article 17 - Right to erasure",
                        "Article 30 - Records of processing"
                    ],
                    "compliance_deadline": "Ongoing",
                    "jurisdiction": "European Union"
                })
            elif regulation.upper() == "HIPAA":
                regulation_data.update({
                    "key_rules": [
                        "Privacy Rule - PHI protection",
                        "Security Rule - Safeguards",
                        "Breach Notification Rule"
                    ],
                    "compliance_deadline": "Ongoing", 
                    "jurisdiction": "United States"
                })
            elif regulation.upper() == "SOX":
                regulation_data.update({
                    "key_sections": [
                        "Section 302 - Financial reporting",
                        "Section 404 - Internal controls",
                        "Section 409 - Real-time disclosure"
                    ],
                    "compliance_deadline": "Annual",
                    "jurisdiction": "United States"
                })
            else:
                regulation_data.update({
                    "description": f"General compliance requirements for {regulation}",
                    "compliance_deadline": "To be determined",
                    "jurisdiction": "Multiple"
                })
                
            return regulation_data
                
        except Exception as e:
            logger.error(f"Error fetching {regulation} data: {e}")
            return {"regulation": regulation, "error": str(e)}
    
    async def detect_regulatory_changes(self) -> Dict[str, Any]:
        """Detect recent regulatory changes"""
        logger.info("Checking for regulatory changes")
        
        # Simulate regulatory change detection
        # In production, this would integrate with real regulatory feeds
        has_changes = random.random() < 0.2  # 20% chance of changes
        
        changes = []
        if has_changes:
            change_regulation = random.choice(self.regulatory_sources)
            change_types = ["guideline_update", "deadline_change", "new_requirement", "clarification"]
            
            changes.append({
                "regulation": change_regulation,
                "change_type": random.choice(change_types),
                "description": f"Updated {change_regulation} compliance requirements",
                "impact_level": random.choice(["low", "medium", "high"]),
                "effective_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "action_required": random.choice([True, False])
            })
            
            logger.info(f"Detected {len(changes)} regulatory changes")

        return {
            "has_changes": has_changes,
            "changes": changes,
            "checked_regulations": self.regulatory_sources,
            "timestamp": datetime.now().isoformat()
        }