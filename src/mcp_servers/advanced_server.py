#!/usr/bin/env python3
"""
Advanced MCP Server Example

Demonstrates advanced MCP features including:
- File operations (read, write, list directories)
- Data analysis tools (CSV processing, statistics)
- System utilities and process management
- Dynamic resource management
"""

import asyncio
import csv
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class AdvancedMCPServer:
    """Advanced MCP server with file operations and data analysis."""
    
    def __init__(self):
        self.server = Server("advanced-mcp-server")
        self.temp_dir = tempfile.mkdtemp(prefix="mcp_")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up MCP handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            tools = [
                types.Tool(
                    name="file_read",
                    description="Read contents of a file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path to read"},
                            "encoding": {"type": "string", "default": "utf-8", "description": "File encoding"}
                        },
                        "required": ["path"]
                    }
                ),
                types.Tool(
                    name="file_write",
                    description="Write content to a file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path to write"},
                            "content": {"type": "string", "description": "Content to write"},
                            "encoding": {"type": "string", "default": "utf-8"}
                        },
                        "required": ["path", "content"]
                    }
                ),
                types.Tool(
                    name="directory_list",
                    description="List directory contents",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Directory path to list"},
                            "show_hidden": {"type": "boolean", "default": False}
                        },
                        "required": ["path"]
                    }
                )
            ]
            
            if PANDAS_AVAILABLE:
                tools.extend([
                    types.Tool(
                        name="csv_analyze",
                        description="Analyze CSV file and provide statistics",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "CSV file path"},
                                "delimiter": {"type": "string", "default": ","}
                            },
                            "required": ["path"]
                        }
                    ),
                    types.Tool(
                        name="data_summary",
                        description="Generate summary statistics for dataset",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "Data file path"},
                                "columns": {"type": "array", "items": {"type": "string"}, "description": "Specific columns to analyze"}
                            },
                            "required": ["path"]
                        }
                    )
                ])
            
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            try:
                if name == "file_read":
                    path = arguments["path"]
                    encoding = arguments.get("encoding", "utf-8")
                    
                    if not os.path.exists(path):
                        return [types.TextContent(type="text", text=f"File not found: {path}")]
                    
                    with open(path, 'r', encoding=encoding) as f:
                        content = f.read()
                    
                    return [types.TextContent(
                        type="text",
                        text=f"File: {path}\nSize: {len(content)} characters\n\nContent:\n{content}"
                    )]
                
                elif name == "file_write":
                    path = arguments["path"]
                    content = arguments["content"]
                    encoding = arguments.get("encoding", "utf-8")
                    
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    
                    with open(path, 'w', encoding=encoding) as f:
                        f.write(content)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Successfully wrote {len(content)} characters to {path}"
                    )]
                
                elif name == "directory_list":
                    path = arguments["path"]
                    show_hidden = arguments.get("show_hidden", False)
                    
                    if not os.path.exists(path):
                        return [types.TextContent(type="text", text=f"Directory not found: {path}")]
                    
                    items = []
                    for item in os.listdir(path):
                        if not show_hidden and item.startswith('.'):
                            continue
                        
                        item_path = os.path.join(path, item)
                        item_type = "DIR" if os.path.isdir(item_path) else "FILE"
                        size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
                        items.append(f"{item_type:4} {size:>10} {item}")
                    
                    result = f"Directory: {path}\nContents ({len(items)} items):\n\n"
                    result += "\n".join(items)
                    
                    return [types.TextContent(type="text", text=result)]
                
                elif name == "csv_analyze" and PANDAS_AVAILABLE:
                    path = arguments["path"]
                    delimiter = arguments.get("delimiter", ",")
                    
                    df = pd.read_csv(path, delimiter=delimiter)
                    
                    analysis = {
                        "file": path,
                        "shape": df.shape,
                        "columns": list(df.columns),
                        "dtypes": df.dtypes.to_dict(),
                        "null_counts": df.isnull().sum().to_dict(),
                        "basic_stats": df.describe().to_dict()
                    }
                    
                    return [types.TextContent(
                        type="text",
                        text=f"CSV Analysis:\n{json.dumps(analysis, indent=2, default=str)}"
                    )]
                
                else:
                    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
                    
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[types.Resource]:
            return [
                types.Resource(
                    uri=AnyUrl("advanced://capabilities"),
                    name="Server Capabilities",
                    description="Advanced server features and capabilities",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri=AnyUrl("advanced://temp_workspace"),
                    name="Temporary Workspace",
                    description="Information about temporary workspace",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            if str(uri) == "advanced://capabilities":
                capabilities = {
                    "file_operations": ["read", "write", "list_directory"],
                    "data_analysis": ["csv_analysis", "statistics"] if PANDAS_AVAILABLE else ["basic_analysis"],
                    "pandas_available": PANDAS_AVAILABLE,
                    "temporary_workspace": self.temp_dir,
                    "supported_formats": ["txt", "csv", "json"],
                    "features": {
                        "file_encoding_support": True,
                        "directory_traversal": True,
                        "statistical_analysis": PANDAS_AVAILABLE
                    }
                }
                return json.dumps(capabilities, indent=2)
            
            elif str(uri) == "advanced://temp_workspace":
                workspace_info = {
                    "path": self.temp_dir,
                    "exists": os.path.exists(self.temp_dir),
                    "files": os.listdir(self.temp_dir) if os.path.exists(self.temp_dir) else [],
                    "created": datetime.now().isoformat()
                }
                return json.dumps(workspace_info, indent=2)
            
            raise ValueError(f"Unknown resource: {uri}")
    
    async def run(self):
        """Run the server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, NotificationOptions())


def main():
    """Main entry point."""
    print("Starting Advanced MCP Server...", file=sys.stderr)
    if not PANDAS_AVAILABLE:
        print("Warning: pandas not available. Data analysis features limited.", file=sys.stderr)
    
    server = AdvancedMCPServer()
    asyncio.run(server.run())


# Export the class for importing
__all__ = ["AdvancedMCPServer"]


if __name__ == "__main__":
    main()