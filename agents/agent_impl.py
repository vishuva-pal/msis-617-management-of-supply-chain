"""
Mock Agent implementation for ComplianceGuard AI
"""

from typing import Dict, List, Any, Callable
import logging

logger = logging.getLogger(__name__)


class Agent:
    """Simple Agent implementation for demo purposes"""
    
    def __init__(self, name: str, model: str, tools: List = None, description: str = ""):
        self.name = name
        self.model = model
        self.tools = tools or []
        self.description = description
        self.session = None
        logger.info(f"Initialized Agent: {name} with model: {model}")
    
    async def start_session(self):
        """Start a new session"""
        self.session = AgentSession(self.name, self.model)
        return self.session


class Tool:
    """Simple Tool implementation"""
    
    def __init__(self, name: str, description: str = "", func: Callable = None):
        self.name = name
        self.description = description
        self.func = func
        logger.info(f"Initialized Tool: {name}")
    
    async def execute(self, *args, **kwargs):
        """Execute the tool"""
        if self.func:
            return self.func(*args, **kwargs)
        return {"status": "success", "tool": self.name}


class AgentSession:
    """Simple Agent Session implementation"""
    
    def __init__(self, agent_name: str, model: str):
        self.agent_name = agent_name
        self.model = model
        self.messages = []
        logger.info(f"Session started for agent: {agent_name}")
    
    async def send_message(self, message: str) -> Dict[str, Any]:
        """Send a message to the agent"""
        self.messages.append(message)
        
        # Return a mock response
        response = {
            "agent": self.agent_name,
            "model": self.model,
            "message": message,
            "response": f"Processed by {self.agent_name}",
            "status": "success"
        }
        
        logger.info(f"Agent {self.agent_name} responded to message")
        return response
    
    async def close(self):
        """Close the session"""
        logger.info(f"Session closed for agent: {self.agent_name}")
