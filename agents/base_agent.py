"""
Base Agent Class - Common functionality for all compliance agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .agent_impl import Agent
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseComplianceAgent(ABC):
    """Base class for all compliance agents"""
    
    def __init__(self, name: str, config: Dict, tools: Dict):
        self.name = name
        self.config = config
        self.tools = tools
        self.agent_config = config['agents'].get(name, {})
        self.model = self.agent_config.get('model', 'gemini-2.0-flash-exp')
        
        # Initialize ADK agent
        self.agent = Agent(
            name=name,
            model=self.model,
            tools=self._initialize_agent_tools(),
            description=self._get_agent_description()
        )
        
        self.session = None
        self.metrics = {
            "requests_processed": 0,
            "errors": 0,
            "last_activity": None
        }
    
    def _initialize_agent_tools(self) -> List:
        """Initialize tools specific to this agent"""
        agent_tools_config = self.agent_config.get('tools', [])
        tools = []
        
        for tool_name in agent_tools_config:
            if tool_name in self.tools:
                tools.append(self.tools[tool_name])
            else:
                logger.warning(f"Tool {tool_name} not found for agent {self.name}")
        
        return tools
    
    def _get_agent_description(self) -> str:
        """Get agent description based on role"""
        descriptions = {
            'regulation_monitor': 'Monitors regulatory changes across GDPR, HIPAA, SOX and alerts on compliance impacts',
            'compliance_analyzer': 'Analyzes company policies against regulatory requirements and identifies compliance gaps', 
            'risk_assessor': 'Assesses compliance risks using ML scoring and provides mitigation recommendations',
            'report_generator': 'Generates comprehensive compliance reports and audit-ready documentation'
        }
        return descriptions.get(self.name, f"{self.name} compliance agent")
    
    async def start_session(self):
        """Start a new agent session"""
        if self.session:
            await self.session.close()
        
        self.session = await self.agent.start_session()
        logger.info(f"Started new session for {self.name}")
        return self.session
    
    async def process(self, input_data: Dict) -> Dict:
        """Process input data using the agent"""
        if not self.session:
            await self.start_session()
        
        try:
            self.metrics["requests_processed"] += 1
            self.metrics["last_activity"] = datetime.now()
            
            logger.info(f"Agent {self.name} processing request")
            response = await self.session.send_message(str(input_data))
            
            parsed_response = self._parse_agent_response(response)
            logger.info(f"Agent {self.name} completed processing")
            
            return parsed_response
            
        except Exception as e:
            self.metrics["errors"] += 1
            logger.error(f"Agent {self.name} processing error: {e}")
            raise
    
    def _parse_agent_response(self, response) -> Dict:
        """Parse agent response into structured format"""
        return {
            "raw_response": response,
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "metrics": self.metrics.copy()
        }
    
    def get_metrics(self) -> Dict:
        """Get agent performance metrics"""
        return self.metrics.copy()
    
    async def shutdown(self):
        """Cleanup agent resources"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info(f"Agent {self.name} shut down")
    
    @abstractmethod
    async def execute_task(self, task_data: Dict) -> Dict:
        """Execute agent-specific task - to be implemented by subclasses"""
        pass