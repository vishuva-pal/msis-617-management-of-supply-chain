"""
Session Management for Compliance Workflows
Manage agent sessions and context preservation
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages agent sessions for compliance workflows
    Provides session persistence and context management
    """
    
    def __init__(self, session_timeout_minutes: int = 60, max_sessions: int = 1000):
        self.session_timeout_minutes = session_timeout_minutes
        self.max_sessions = max_sessions
        self.active_sessions = {}
        self.session_history = {}
        
        # Session cleanup task
        self.cleanup_task = None
        
    async def start(self):
        """Start session manager and cleanup task"""
        logger.info("Starting session manager")
        self.cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def stop(self):
        """Stop session manager and cleanup"""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Close all active sessions
        for session_id in list(self.active_sessions.keys()):
            await self.end_session(session_id)
        
        logger.info("Session manager stopped")
    
    async def create_session(self, company_id: str, workflow_type: str = "compliance_check") -> str:
        """
        Create a new compliance workflow session
        
        Args:
            company_id: Company identifier
            workflow_type: Type of workflow
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "company_id": company_id,
            "workflow_type": workflow_type,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "status": "active",
            "context": {
                "current_step": "initialized",
                "workflow_progress": 0,
                "agent_interactions": [],
                "compliance_data": {},
                "errors_encountered": []
            },
            "metrics": {
                "agents_used": [],
                "processing_time": 0,
                "data_points_collected": 0
            }
        }
        
        self.active_sessions[session_id] = session_data
        
        logger.info(f"Created session {session_id} for company {company_id}")
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data if found
        """
        session = self.active_sessions.get(session_id)
        if session:
            # Update last activity
            session["last_activity"] = datetime.now().isoformat()
            return session
        
        # Check session history
        return self.session_history.get(session_id)
    
    async def update_session_context(self, session_id: str, context_updates: Dict[str, Any]) -> bool:
        """
        Update session context
        
        Args:
            session_id: Session identifier
            context_updates: Context data to update
            
        Returns:
            Success status
        """
        session = await self.get_session(session_id)
        if not session:
            logger.warning(f"Session {session_id} not found for update")
            return False
        
        # Merge context updates
        for key, value in context_updates.items():
            if key in session["context"] and isinstance(session["context"][key], dict) and isinstance(value, dict):
                session["context"][key].update(value)
            else:
                session["context"][key] = value
        
        session["last_activity"] = datetime.now().isoformat()
        
        logger.debug(f"Updated context for session {session_id}")
        return True
    
    async def record_agent_interaction(self, session_id: str, agent_name: str, 
                                    input_data: Dict, output_data: Dict) -> bool:
        """
        Record agent interaction in session
        
        Args:
            session_id: Session identifier
            agent_name: Name of the agent
            input_data: Input provided to agent
            output_data: Output from agent
            
        Returns:
            Success status
        """
        session = await self.get_session(session_id)
        if not session:
            return False
        
        interaction = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "input_summary": self._summarize_input(input_data),
            "output_summary": self._summarize_output(output_data),
            "processing_time_ms": random.randint(100, 5000)  # Simulated
        }
        
        session["context"]["agent_interactions"].append(interaction)
        session["metrics"]["agents_used"].append(agent_name)
        
        # Update workflow progress based on agent completion
        self._update_workflow_progress(session, agent_name)
        
        logger.debug(f"Recorded {agent_name} interaction for session {session_id}")
        return True
    
    async def end_session(self, session_id: str, status: str = "completed") -> bool:
        """
        End a session and move to history
        
        Args:
            session_id: Session identifier
            status: Final session status
            
        Returns:
            Success status
        """
        session = self.active_sessions.pop(session_id, None)
        if not session:
            logger.warning(f"Session {session_id} not found for ending")
            return False
        
        # Update session end data
        session["ended_at"] = datetime.now().isoformat()
        session["status"] = status
        session["final_metrics"] = self._calculate_final_metrics(session)
        
        # Move to history
        self.session_history[session_id] = session
        
        logger.info(f"Ended session {session_id} with status: {status}")
        return True
    
    async def get_session_metrics(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metrics for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session metrics if found
        """
        session = await self.get_session(session_id)
        if not session:
            return None
        
        return session.get("metrics", {})
    
    async def get_workflow_sessions(self, company_id: str, 
                                  workflow_type: str = None) -> List[Dict[str, Any]]:
        """
        Get sessions for a company and optional workflow type
        
        Args:
            company_id: Company identifier
            workflow_type: Optional workflow type filter
            
        Returns:
            List of session data
        """
        sessions = []
        
        # Check active sessions
        for session in self.active_sessions.values():
            if session["company_id"] == company_id:
                if not workflow_type or session["workflow_type"] == workflow_type:
                    sessions.append(session)
        
        # Check session history
        for session in self.session_history.values():
            if session["company_id"] == company_id:
                if not workflow_type or session["workflow_type"] == workflow_type:
                    sessions.append(session)
        
        # Sort by creation time (newest first)
        sessions.sort(key=lambda x: x["created_at"], reverse=True)
        
        return sessions
    
    def _summarize_input(self, input_data: Dict) -> Dict:
        """Create summary of agent input data"""
        return {
            "data_type": type(input_data).__name__,
            "size_estimate": len(str(input_data)),
            "has_company_data": "company_id" in str(input_data),
            "has_regulatory_data": any(reg in str(input_data) for reg in ["GDPR", "HIPAA", "SOX"])
        }
    
    def _summarize_output(self, output_data: Dict) -> Dict:
        """Create summary of agent output data"""
        return {
            "data_type": type(output_data).__name__,
            "size_estimate": len(str(output_data)),
            "has_compliance_score": "compliance_score" in str(output_data),
            "has_risk_assessment": "risk" in str(output_data).lower(),
            "has_recommendations": "recommendation" in str(output_data).lower()
        }
    
    def _update_workflow_progress(self, session: Dict, agent_name: str):
        """Update workflow progress based on agent completion"""
        workflow_steps = {
            "regulation_monitor": 25,
            "compliance_analyzer": 50, 
            "risk_assessor": 75,
            "report_generator": 100
        }
        
        if agent_name in workflow_steps:
            session["context"]["workflow_progress"] = max(
                session["context"]["workflow_progress"],
                workflow_steps[agent_name]
            )
        
        session["context"]["current_step"] = f"completed_{agent_name}"
    
    def _calculate_final_metrics(self, session: Dict) -> Dict:
        """Calculate final metrics for ended session"""
        interactions = session["context"]["agent_interactions"]
        
        return {
            "total_agents_used": len(set(session["metrics"]["agents_used"])),
            "total_interactions": len(interactions),
            "average_processing_time": sum(
                i.get("processing_time_ms", 0) for i in interactions
            ) / len(interactions) if interactions else 0,
            "session_duration_minutes": (
                datetime.fromisoformat(session["ended_at"].replace('Z', '+00:00')) - 
                datetime.fromisoformat(session["created_at"].replace('Z', '+00:00'))
            ).total_seconds() / 60,
            "success_rate": 100 if session["status"] == "completed" else 0
        }
    
    async def _cleanup_loop(self):
        """Background task to clean up expired sessions"""
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                await self._cleanup_expired_sessions()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Session cleanup error: {e}")
    
    async def _cleanup_expired_sessions(self):
        """Clean up sessions that have timed out"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            last_activity = datetime.fromisoformat(session["last_activity"].replace('Z', '+00:00'))
            time_since_activity = (current_time - last_activity).total_seconds() / 60
            
            if time_since_activity > self.session_timeout_minutes:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            logger.info(f"Cleaning up expired session: {session_id}")
            await self.end_session(session_id, "timeout")
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")