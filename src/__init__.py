"""
MCP Data Analysis Toolkit

A comprehensive Python toolkit for Model Context Protocol (MCP) implementation
with specialized focus on data analysis and business intelligence workflows.

Created by Vijay Andem - Data Analyst passionate about transforming complex 
datasets into compelling visual stories.

Features:
- Production-ready MCP servers for data analysis
- Claude Desktop integration
- Specialized tools for Power BI, Tableau, and Streamlit workflows
- Comprehensive data analysis capabilities

Author: Vijay Andem
LinkedIn: https://www.linkedin.com/in/vijay-andem-b2092223/
Twitter: https://x.com/vjandem
"""

__version__ = "1.0.0"
__author__ = "Vijay Andem"
__email__ = "your.email@example.com"
__description__ = "MCP Data Analysis Toolkit for AI-powered business intelligence"

from .mcp_servers import *
from .clients import *

__all__ = [
    "BasicMCPServer",
    "AdvancedMCPServer", 
    "DataAnalysisMCPServer",
    "MCPClientExample"
]