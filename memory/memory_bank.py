"""
Memory Bank for Compliance Context
Long-term memory storage with context compaction
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class ComplianceMemoryBank:
    """
    Memory bank for storing compliance context, history, and patterns
    Implements context compaction and long-term memory management
    """
    
    def __init__(self, max_entries: int = 10000, compaction_strategy: str = "semantic"):
        self.max_entries = max_entries
        self.compaction_strategy = compaction_strategy
        self.memory_store = {}
        self.audit_trail = []
        self.compliance_patterns = {}
        self.risk_profiles = {}
        
        # Memory metrics
        self.metrics = {
            "total_stored": 0,
            "compactions_performed": 0,
            "memory_usage_mb": 0,
            "last_compaction": None
        }
    
    async def store_compliance_check(self, company_id: str, compliance_data: Dict[str, Any]) -> str:
        """
        Store compliance check results in memory bank
        
        Args:
            company_id: Unique identifier for the company
            compliance_data: Compliance assessment results
            
        Returns:
            Memory entry ID
        """
        entry_id = f"COMP-{company_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        memory_entry = {
            "entry_id": entry_id,
            "company_id": company_id,
            "timestamp": datetime.now().isoformat(),
            "compliance_score": compliance_data.get('executive_summary', {}).get('overall_compliance_score', 0),
            "risk_score": compliance_data.get('executive_summary', {}).get('overall_risk_score', 0),
            "key_findings": self._extract_key_findings(compliance_data),
            "gap_count": len(compliance_data.get('detailed_analysis', {}).get('gap_breakdown', [])),
            "regulation_scores": compliance_data.get('detailed_analysis', {}).get('regulation_performance', {}),
            "raw_data": compliance_data  # Store full data for context
        }
        
        # Store in memory
        if company_id not in self.memory_store:
            self.memory_store[company_id] = []
        
        self.memory_store[company_id].append(memory_entry)
        
        # Update audit trail
        audit_entry = {
            "action": "compliance_check_stored",
            "company_id": company_id,
            "entry_id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "compliance_score": memory_entry["compliance_score"]
        }
        self.audit_trail.append(audit_entry)
        
        # Update metrics
        self.metrics["total_stored"] += 1
        
        # Check if compaction is needed
        if self._should_compact():
            await self._compact_memory()
        
        logger.info(f"Stored compliance check {entry_id} for company {company_id}")
        
        return entry_id
    
    async def retrieve_compliance_history(self, company_id: str, 
                                       lookback_days: int = 90) -> List[Dict[str, Any]]:
        """
        Retrieve compliance history for a company
        
        Args:
            company_id: Company to retrieve history for
            lookback_days: Number of days to look back
            
        Returns:
            List of compliance history entries
        """
        if company_id not in self.memory_store:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=lookback_days)
        
        history = [
            entry for entry in self.memory_store[company_id]
            if datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00')) >= cutoff_date
        ]
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        logger.info(f"Retrieved {len(history)} compliance history entries for {company_id}")
        
        return history
    
    async def get_compliance_trends(self, company_id: str) -> Dict[str, Any]:
        """
        Analyze compliance trends for a company
        
        Args:
            company_id: Company to analyze
            
        Returns:
            Dictionary containing trend analysis
        """
        history = await self.retrieve_compliance_history(company_id, lookback_days=180)
        
        if not history:
            return {"error": "No compliance history found"}
        
        # Calculate trends
        scores = [entry["compliance_score"] for entry in history]
        risk_scores = [entry["risk_score"] for entry in history]
        
        if len(scores) >= 2:
            score_trend = "improving" if scores[0] > scores[-1] else "declining" if scores[0] < scores[-1] else "stable"
            risk_trend = "improving" if risk_scores[0] < risk_scores[-1] else "declining" if risk_scores[0] > risk_scores[-1] else "stable"
        else:
            score_trend = "insufficient_data"
            risk_trend = "insufficient_data"
        
        # Identify recurring gaps
        all_gaps = []
        for entry in history:
            if "key_findings" in entry:
                all_gaps.extend(entry["key_findings"].get("high_priority_gaps", []))
        
        # Find most common gaps
        from collections import Counter
        gap_counter = Counter(all_gaps)
        recurring_gaps = gap_counter.most_common(5)
        
        return {
            "company_id": company_id,
            "analysis_period": f"Last {len(history)} assessments",
            "current_score": scores[0] if scores else 0,
            "average_score": sum(scores) / len(scores) if scores else 0,
            "score_trend": score_trend,
            "risk_trend": risk_trend,
            "recurring_gaps": [gap for gap, count in recurring_gaps],
            "improvement_areas": self._identify_improvement_areas(history),
            "confidence_in_trends": min(95, len(history) * 10),  # More history = more confidence
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def store_compliance_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]) -> str:
        """
        Store compliance patterns for cross-company insights
        
        Args:
            pattern_type: Type of pattern (e.g., 'industry_trends', 'common_gaps')
            pattern_data: Pattern data to store
            
        Returns:
            Pattern ID
        """
        pattern_id = f"PATTERN-{pattern_type}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        pattern_entry = {
            "pattern_id": pattern_id,
            "pattern_type": pattern_type,
            "timestamp": datetime.now().isoformat(),
            "data": pattern_data,
            "confidence_score": pattern_data.get('confidence', 0.8),
            "applicability": pattern_data.get('applicability', 'general')
        }
        
        if pattern_type not in self.compliance_patterns:
            self.compliance_patterns[pattern_type] = []
        
        self.compliance_patterns[pattern_type].append(pattern_entry)
        
        logger.info(f"Stored compliance pattern {pattern_id} of type {pattern_type}")
        
        return pattern_id
    
    async def get_industry_benchmarks(self, industry: str, regulation: str) -> Optional[Dict[str, Any]]:
        """
        Get industry benchmarks for specific regulations
        
        Args:
            industry: Industry to get benchmarks for
            regulation: Specific regulation
            
        Returns:
            Benchmark data if available
        """
        # This would typically query an external benchmark database
        # For now, return mock data
        
        benchmarks = {
            "technology": {
                "GDPR": {"average_score": 82, "top_performers": 95, "common_challenges": ["data_mapping", "consent_management"]},
                "SOX": {"average_score": 88, "top_performers": 96, "common_challenges": ["internal_controls", "documentation"]}
            },
            "healthcare": {
                "HIPAA": {"average_score": 85, "top_performers": 98, "common_challenges": ["phi_protection", "breach_response"]},
                "GDPR": {"average_score": 78, "top_performers": 92, "common_challenges": ["cross_border_transfers", "patient_rights"]}
            },
            "finance": {
                "SOX": {"average_score": 90, "top_performers": 98, "common_challenges": ["financial_reporting", "audit_trails"]},
                "GDPR": {"average_score": 80, "top_performers": 94, "common_challenges": ["customer_data", "consent_management"]}
            }
        }
        
        industry_benchmarks = benchmarks.get(industry.lower(), {}).get(regulation.upper())
        
        if industry_benchmarks:
            return {
                "industry": industry,
                "regulation": regulation,
                "benchmarks": industry_benchmarks,
                "data_source": "ComplianceGuard AI Industry Database",
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
        
        return None
    
    def _extract_key_findings(self, compliance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key findings from compliance data for memory storage"""
        executive_summary = compliance_data.get('executive_summary', {})
        detailed_analysis = compliance_data.get('detailed_analysis', {})
        
        return {
            "overall_score": executive_summary.get('overall_compliance_score', 0),
            "risk_level": executive_summary.get('compliance_status', 'unknown'),
            "high_priority_gaps": [
                gap for gap in detailed_analysis.get('gap_breakdown', {}).values() 
                if isinstance(gap, list) and any(g.get('severity') == 'high' for g in gap)
            ],
            "top_regulations": list(detailed_analysis.get('regulation_performance', {}).keys())[:3],
            "recommendation_count": len(compliance_data.get('recommendations', {}).get('immediate_actions', []))
        }
    
    def _should_compact(self) -> bool:
        """Check if memory compaction is needed"""
        total_entries = sum(len(entries) for entries in self.memory_store.values())
        return total_entries > self.max_entries
    
    async def _compact_memory(self):
        """Perform memory compaction to manage storage"""
        logger.info("Performing memory compaction")
        
        for company_id, entries in self.memory_store.items():
            if len(entries) > 100:  # Keep last 100 entries per company
                # Keep high-risk entries and recent entries
                high_risk_entries = [
                    entry for entry in entries 
                    if entry.get('compliance_score', 0) < 70 or 
                       any('high' in str(gap).lower() for gap in entry.get('key_findings', {}).get('high_priority_gaps', []))
                ]
                
                recent_entries = sorted(entries, key=lambda x: x['timestamp'], reverse=True)[:50]
                
                # Combine and deduplicate
                compacted_entries = list({entry['entry_id']: entry for entry in high_risk_entries + recent_entries}.values())
                self.memory_store[company_id] = compacted_entries
        
        self.metrics["compactions_performed"] += 1
        self.metrics["last_compaction"] = datetime.now().isoformat()
        
        logger.info("Memory compaction completed")
    
    def _identify_improvement_areas(self, history: List[Dict]) -> List[str]:
        """Identify areas for improvement from historical data"""
        if not history:
            return []
        
        # Analyze gap patterns across history
        all_gaps = []
        for entry in history:
            if "key_findings" in entry:
                all_gaps.extend(entry["key_findings"].get("high_priority_gaps", []))
        
        from collections import Counter
        gap_frequency = Counter(all_gaps)
        
        improvement_areas = []
        for gap, frequency in gap_frequency.most_common(3):
            if frequency >= 2:  # Appears in at least 2 assessments
                improvement_areas.append(f"Address recurring gap: {gap}")
        
        return improvement_areas
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """Get memory bank metrics"""
        total_entries = sum(len(entries) for entries in self.memory_store.values())
        total_patterns = sum(len(patterns) for patterns in self.compliance_patterns.values())
        
        return {
            **self.metrics,
            "current_entries": total_entries,
            "companies_tracked": len(self.memory_store),
            "patterns_stored": total_patterns,
            "audit_trail_entries": len(self.audit_trail),
            "memory_health": "good" if total_entries < self.max_entries * 0.8 else "needs_compaction"
        }