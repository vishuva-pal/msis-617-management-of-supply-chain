"""
Report Generator Agent - Creates compliance reports
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime
import json

from .base_agent import BaseComplianceAgent

logger = logging.getLogger(__name__)

class ReportGeneratorAgent(BaseComplianceAgent):
    """Generates comprehensive compliance reports"""
    
    def __init__(self, config: Dict, tools: Dict):
        super().__init__("report_generator", config, tools)
        self.report_templates = self._load_report_templates()
        
    async def execute_task(self, task_data: Dict) -> Dict:
        """Execute report generation task"""
        analysis_results = task_data.get('analysis_results', {})
        risk_assessment = task_data.get('risk_assessment', {})
        
        return await self.generate_report(analysis_results, risk_assessment)
        
    async def generate_report(self, analysis_results: Dict, risk_assessment: Dict) -> Dict:
        """Generate comprehensive compliance report"""
        logger.info("Generating compliance report")
        
        await asyncio.sleep(0.4)  # Simulate report generation
        
        report = {
            "report_id": f"COMP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "executive_summary": {},
            "detailed_analysis": {},
            "recommendations": {},
            "action_plan": {},
            "compliance_metrics": {},
            "audit_readiness": {},
            "generated_at": datetime.now().isoformat(),
            "report_version": "1.0"
        }
        
        # Generate executive summary
        report["executive_summary"] = self._generate_executive_summary(analysis_results, risk_assessment)
        
        # Generate detailed analysis
        report["detailed_analysis"] = self._generate_detailed_analysis(analysis_results)
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(analysis_results, risk_assessment)
        
        # Generate action plan
        report["action_plan"] = self._generate_action_plan(analysis_results, risk_assessment)
        
        # Generate compliance metrics
        report["compliance_metrics"] = self._generate_compliance_metrics(analysis_results)
        
        # Generate audit readiness assessment
        report["audit_readiness"] = self._generate_audit_readiness(analysis_results)
        
        logger.info(f"Compliance report generated: {report['report_id']}")
        
        return report
    
    def _generate_executive_summary(self, analysis_results: Dict, risk_assessment: Dict) -> Dict:
        """Generate executive summary"""
        overall_score = analysis_results.get('overall_score', 0)
        risk_score = risk_assessment.get('overall_risk_score', 0)
        
        return {
            "overall_compliance_score": overall_score,
            "overall_risk_score": risk_score,
            "compliance_status": self._get_compliance_status(overall_score),
            "key_findings": [
                f"Overall compliance score: {overall_score}%",
                f"Identified {len(analysis_results.get('gap_analysis', []))} compliance gaps",
                f"High-risk areas: {len([g for g in analysis_results.get('gap_analysis', []) if g.get('severity') == 'high'])}"
            ],
            "priority_actions": [
                "Address high-severity compliance gaps",
                "Implement recommended controls",
                "Schedule follow-up assessment"
            ]
        }
    
    def _generate_detailed_analysis(self, analysis_results: Dict) -> Dict:
        """Generate detailed compliance analysis"""
        regulation_scores = analysis_results.get('regulation_scores', {})
        gap_analysis = analysis_results.get('gap_analysis', [])
        
        detailed_analysis = {
            "regulation_performance": {},
            "gap_breakdown": {},
            "strengths_weaknesses": {}
        }
        
        # Regulation performance
        for regulation, score in regulation_scores.items():
            detailed_analysis["regulation_performance"][regulation] = {
                "score": score,
                "status": self._get_compliance_status(score),
                "benchmark": "Industry Average: 85%",
                "trend": "stable"
            }
        
        # Gap breakdown
        gap_by_regulation = {}
        for gap in gap_analysis:
            regulation = gap.get('regulation')
            if regulation not in gap_by_regulation:
                gap_by_regulation[regulation] = []
            gap_by_regulation[regulation].append(gap)
        
        detailed_analysis["gap_breakdown"] = gap_by_regulation
        
        # Strengths and weaknesses
        strengths = [reg for reg, score in regulation_scores.items() if score >= 85]
        weaknesses = [reg for reg, score in regulation_scores.items() if score < 75]
        
        detailed_analysis["strengths_weaknesses"] = {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement_areas": weaknesses
        }
        
        return detailed_analysis
    
    def _generate_recommendations(self, analysis_results: Dict, risk_assessment: Dict) -> Dict:
        """Generate recommendations section"""
        recommendations = analysis_results.get('recommendations', [])
        mitigation_strategies = risk_assessment.get('mitigation_strategies', [])
        
        return {
            "immediate_actions": [
                rec for rec in recommendations if rec.get('priority') == 'high'
            ][:3],
            "short_term_actions": [
                rec for rec in recommendations if rec.get('priority') == 'medium'
            ][:5],
            "long_term_strategies": mitigation_strategies,
            "resource_allocation": {
                "high_priority": "Allocate immediate resources",
                "medium_priority": "Plan for next quarter",
                "low_priority": "Monitor and review"
            }
        }
    
    def _generate_action_plan(self, analysis_results: Dict, risk_assessment: Dict) -> Dict:
        """Generate actionable compliance plan"""
        gaps = analysis_results.get('gap_analysis', [])
        high_priority_gaps = [gap for gap in gaps if gap.get('severity') == 'high']
        
        return {
            "timeline": {
                "immediate": ["Address critical gaps", "Implement urgent controls"],
                "30_days": ["Medium priority fixes", "Documentation updates"],
                "90_days": ["Process improvements", "Training programs"]
            },
            "responsibilities": {
                "compliance_team": ["Gap remediation", "Policy updates"],
                "it_department": ["Technical controls", "System configurations"],
                "hr_department": ["Training programs", "Policy communication"]
            },
            "success_metrics": {
                "compliance_score_target": "90%",
                "gap_reduction_target": "80%",
                "audit_readiness_target": "Fully prepared"
            }
        }
    
    def _generate_compliance_metrics(self, analysis_results: Dict) -> Dict:
        """Generate compliance metrics dashboard"""
        regulation_scores = analysis_results.get('regulation_scores', {})
        
        return {
            "current_performance": {
                "overall_score": analysis_results.get('overall_score', 0),
                "regulation_count": len(regulation_scores),
                "gaps_identified": len(analysis_results.get('gap_analysis', [])),
                "high_risk_gaps": len([g for g in analysis_results.get('gap_analysis', []) if g.get('severity') == 'high'])
            },
            "trends": {
                "compliance_trend": "improving",
                "risk_trend": "decreasing", 
                "efficiency_trend": "improving"
            },
            "benchmarks": {
                "industry_average": 85,
                "regulatory_requirements": 100,
                "internal_target": 90
            }
        }
    
    def _generate_audit_readiness(self, analysis_results: Dict) -> Dict:
        """Generate audit readiness assessment"""
        overall_score = analysis_results.get('overall_score', 0)
        
        if overall_score >= 90:
            readiness = "fully_prepared"
        elif overall_score >= 80:
            readiness = "mostly_prepared" 
        elif overall_score >= 70:
            readiness = "partially_prepared"
        else:
            readiness = "not_prepared"
        
        return {
            "readiness_level": readiness,
            "documentation_status": "complete" if overall_score >= 80 else "partial",
            "evidence_availability": "available" if overall_score >= 85 else "needs_work",
            "recommended_preparations": [
                "Organize compliance documentation",
                "Prepare evidence for key controls",
                "Conduct mock audit"
            ]
        }
    
    def _get_compliance_status(self, score: int) -> str:
        """Get compliance status from score"""
        if score >= 90:
            return "excellent"
        elif score >= 80:
            return "good"
        elif score >= 70:
            return "fair"
        else:
            return "needs_improvement"
    
    def _load_report_templates(self) -> Dict:
        """Load report templates"""
        return {
            "executive_summary": {
                "sections": ["overview", "key_metrics", "priority_actions"],
                "format": "narrative"
            },
            "detailed_analysis": {
                "sections": ["regulation_performance", "gap_analysis", "risk_assessment"],
                "format": "structured"
            },
            "action_plan": {
                "sections": ["timeline", "responsibilities", "metrics"],
                "format": "tabular"
            }
        }