"""
Risk Assessment Agent - Evaluates compliance risks
"""

import asyncio
import logging
from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

from .base_agent import BaseComplianceAgent

logger = logging.getLogger(__name__)

class RiskAssessmentAgent(BaseComplianceAgent):
    """Assesses compliance risks and provides scoring"""
    
    def __init__(self, config: Dict, tools: Dict):
        super().__init__("risk_assessor", config, tools)
        self.risk_history = []
        
    async def execute_task(self, task_data: Dict) -> Dict:
        """Execute risk assessment task"""
        analysis_results = task_data.get('analysis_results', {})
        return await self.assess_risk(analysis_results)
        
    async def assess_risk(self, analysis_results: Dict) -> Dict:
        """Assess compliance risks based on analysis results"""
        logger.info("Starting risk assessment")
        
        await asyncio.sleep(0.3)  # Simulate processing
        
        risk_assessment = {
            "overall_risk_score": 0,
            "risk_breakdown": {},
            "risk_factors": [],
            "mitigation_strategies": [],
            "compliance_health": {},
            "predicted_risks": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Calculate overall risk score
        overall_score = analysis_results.get('overall_score', 0)
        risk_assessment["overall_risk_score"] = self._calculate_risk_score(overall_score)
        
        # Analyze regulation-specific risks
        regulation_scores = analysis_results.get('regulation_scores', {})
        for regulation, score in regulation_scores.items():
            risk_assessment["risk_breakdown"][regulation] = {
                "score": score,
                "risk_level": self._get_risk_level(score),
                "weighted_risk": self._calculate_weighted_risk(regulation, score)
            }
        
        # Identify risk factors
        gaps = analysis_results.get('gap_analysis', [])
        risk_assessment["risk_factors"] = self._identify_risk_factors(gaps)
        
        # Generate mitigation strategies
        risk_assessment["mitigation_strategies"] = self._generate_mitigation_strategies(
            risk_assessment["risk_factors"]
        )
        
        # Assess compliance health
        risk_assessment["compliance_health"] = self._assess_compliance_health(analysis_results)
        
        # Predict future risks
        risk_assessment["predicted_risks"] = self._predict_future_risks(analysis_results)
        
        # Store in history
        self.risk_history.append(risk_assessment)
        
        logger.info(f"Risk assessment completed. Overall risk score: {risk_assessment['overall_risk_score']}")
        
        return risk_assessment
    
    def _calculate_risk_score(self, compliance_score: int) -> int:
        """Calculate risk score from compliance score"""
        return max(0, 100 - compliance_score)
    
    def _get_risk_level(self, score: int) -> str:
        """Get risk level from score"""
        if score >= 90:
            return "low"
        elif score >= 75:
            return "medium"
        elif score >= 60:
            return "high"
        else:
            return "critical"
    
    def _calculate_weighted_risk(self, regulation: str, score: int) -> float:
        """Calculate weighted risk based on regulation importance"""
        weights = {
            "GDPR": 1.2,  # Higher weight due to potential fines
            "HIPAA": 1.1,  # Higher weight due to healthcare implications
            "SOX": 1.15,   # Higher weight due to financial reporting
        }
        weight = weights.get(regulation.upper(), 1.0)
        return (100 - score) * weight
    
    def _identify_risk_factors(self, gaps: List[Dict]) -> List[Dict]:
        """Identify key risk factors from compliance gaps"""
        risk_factors = []
        
        high_severity_gaps = [gap for gap in gaps if gap.get('severity') == 'high']
        medium_severity_gaps = [gap for gap in gaps if gap.get('severity') == 'medium']
        
        if high_severity_gaps:
            risk_factors.append({
                "type": "high_severity_gaps",
                "count": len(high_severity_gaps),
                "impact": "high",
                "description": f"{len(high_severity_gaps)} high severity compliance gaps identified"
            })
        
        if medium_severity_gaps:
            risk_factors.append({
                "type": "medium_severity_gaps", 
                "count": len(medium_severity_gaps),
                "impact": "medium",
                "description": f"{len(medium_severity_gaps)} medium severity compliance gaps identified"
            })
        
        # Add some general risk factors
        general_risks = [
            {
                "type": "regulatory_changes",
                "impact": "medium",
                "description": "Potential regulatory changes in next 6 months",
                "probability": "medium"
            },
            {
                "type": "staff_training",
                "impact": "low",
                "description": "Compliance training completion rate below target",
                "probability": "high"
            }
        ]
        
        risk_factors.extend(general_risks)
        return risk_factors
    
    def _generate_mitigation_strategies(self, risk_factors: List[Dict]) -> List[Dict]:
        """Generate mitigation strategies for identified risks"""
        strategies = []
        
        for risk in risk_factors:
            if risk["type"] == "high_severity_gaps":
                strategies.append({
                    "risk_type": risk["type"],
                    "strategy": "Immediate gap remediation",
                    "priority": "critical",
                    "timeline": "30 days",
                    "resources_needed": ["compliance_team", "technical_staff", "budget"]
                })
            elif risk["type"] == "medium_severity_gaps":
                strategies.append({
                    "risk_type": risk["type"], 
                    "strategy": "Phased gap remediation",
                    "priority": "high",
                    "timeline": "90 days",
                    "resources_needed": ["compliance_team", "department_heads"]
                })
            elif risk["type"] == "regulatory_changes":
                strategies.append({
                    "risk_type": risk["type"],
                    "strategy": "Enhanced regulatory monitoring",
                    "priority": "medium", 
                    "timeline": "Ongoing",
                    "resources_needed": ["monitoring_tools", "legal_review"]
                })
        
        return strategies
    
    def _assess_compliance_health(self, analysis_results: Dict) -> Dict:
        """Assess overall compliance health"""
        overall_score = analysis_results.get('overall_score', 0)
        
        if overall_score >= 90:
            health_status = "excellent"
        elif overall_score >= 80:
            health_status = "good"
        elif overall_score >= 70:
            health_status = "fair"
        else:
            health_status = "poor"
        
        return {
            "status": health_status,
            "score": overall_score,
            "trend": random.choice(["improving", "stable", "declining"]),
            "next_review_recommended": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
    
    def _predict_future_risks(self, analysis_results: Dict) -> List[Dict]:
        """Predict potential future compliance risks"""
        predicted_risks = []
        
        risk_scenarios = [
            {
                "scenario": "New data privacy regulation",
                "probability": "medium",
                "timeframe": "6-12 months", 
                "potential_impact": "high",
                "preparation_recommendation": "Review data handling practices"
            },
            {
                "scenario": "Increased enforcement activity",
                "probability": "high",
                "timeframe": "3-6 months",
                "potential_impact": "medium",
                "preparation_recommendation": "Document compliance efforts"
            },
            {
                "scenario": "Industry-wide compliance audit",
                "probability": "low", 
                "timeframe": "12+ months",
                "potential_impact": "high",
                "preparation_recommendation": "Conduct internal audit"
            }
        ]
        
        return random.sample(risk_scenarios, min(2, len(risk_scenarios)))