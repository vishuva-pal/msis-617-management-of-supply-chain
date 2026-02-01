"""
Tool Setup and Initialization
Configure and initialize all tools for ComplianceGuard AI
"""

import logging
from typing import Dict, Any
from agents.agent_impl import Tool

from .custom_tools import (
    compliance_gap_analyzer,
    risk_scoring_engine,
    policy_analyzer,
    regulatory_search_tool,
    audit_trail_generator,
    compliance_report_formatter
)

from .mcp_tools import (
    regulation_database_tool,
    compliance_framework_tool
)

logger = logging.getLogger(__name__)

def initialize_tools(config: Dict[str, Any]) -> Dict[str, Tool]:
    """
    Initialize and configure all tools for the compliance system
    
    Args:
        config: System configuration dictionary
        
    Returns:
        Dictionary of initialized tools
    """
    logger.info("Initializing compliance tools")
    
    tools_config = config.get('tools', {})
    
    # Initialize custom tools
    tools = {
        'compliance_gap_analyzer': compliance_gap_analyzer,
        'risk_scoring_engine': risk_scoring_engine,
        'policy_analyzer': policy_analyzer,
        'regulatory_search_tool': regulatory_search_tool,
        'audit_trail_generator': audit_trail_generator,
        'compliance_report_formatter': compliance_report_formatter,
        'regulation_database_tool': regulation_database_tool,
        'compliance_framework_tool': compliance_framework_tool
    }
    
    # Apply tool-specific configurations
    for tool_name, tool_config in tools_config.items():
        if tool_name in tools:
            logger.info(f"Configuring tool: {tool_name}")
            # Tool configuration would be applied here
            # For example: tools[tool_name].configure(tool_config)
    
    logger.info(f"Initialized {len(tools)} tools")
    
    return tools