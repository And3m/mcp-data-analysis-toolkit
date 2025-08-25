#!/usr/bin/env python3
"""
Basic MCP Server Example

This script demonstrates a simple MCP server implementation with:
- Basic tools (calculator, string utilities)
- Simple resources (system info, configuration)
- Example prompts for AI interactions

Perfect for understanding MCP fundamentals.
"""

import asyncio
import json
import os
import platform
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl


class BasicMCPServer:
    """A basic MCP server with essential tools and resources."""
    
    def __init__(self):
        self.server = Server("basic-mcp-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up all MCP handlers for tools, resources, and prompts."""
        
        # Tool handlers
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools."""
            return [
                types.Tool(
                    name="calculator",
                    description="Perform basic mathematical calculations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                            }
                        },
                        "required": ["expression"]
                    }
                ),
                types.Tool(
                    name="string_utils",
                    description="String manipulation utilities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to manipulate"
                            },
                            "operation": {
                                "type": "string",
                                "enum": ["uppercase", "lowercase", "reverse", "length", "words"],
                                "description": "Operation to perform on the text"
                            }
                        },
                        "required": ["text", "operation"]
                    }
                ),
                types.Tool(
                    name="get_current_time",
                    description="Get the current date and time",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "format": {
                                "type": "string",
                                "description": "Time format (iso, readable, timestamp)",
                                "enum": ["iso", "readable", "timestamp"],
                                "default": "readable"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            """Handle tool execution."""
            
            if name == "calculator":
                try:
                    expression = arguments.get("expression", "")
                    # Basic safety check
                    if any(dangerous in expression for dangerous in ["import", "exec", "eval", "__"]):
                        raise ValueError("Unsafe expression detected")
                    
                    result = eval(expression)
                    return [
                        types.TextContent(
                            type="text",
                            text=f"Result: {result}\nExpression: {expression}"
                        )
                    ]
                except Exception as e:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"Error calculating '{expression}': {str(e)}"
                        )
                    ]
            
            elif name == "string_utils":
                text = arguments.get("text", "")
                operation = arguments.get("operation", "")
                
                try:
                    if operation == "uppercase":
                        result = text.upper()
                    elif operation == "lowercase":
                        result = text.lower()
                    elif operation == "reverse":
                        result = text[::-1]
                    elif operation == "length":
                        result = f"Length: {len(text)} characters"
                    elif operation == "words":
                        words = text.split()
                        result = f"Word count: {len(words)}\nWords: {words}"
                    else:
                        result = f"Unknown operation: {operation}"
                    
                    return [
                        types.TextContent(
                            type="text",
                            text=f"Operation: {operation}\nInput: {text}\nResult: {result}"
                        )
                    ]
                except Exception as e:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"Error processing text: {str(e)}"
                        )
                    ]
            
            elif name == "get_current_time":
                try:
                    format_type = arguments.get("format", "readable")
                    now = datetime.now()
                    
                    if format_type == "iso":
                        result = now.isoformat()
                    elif format_type == "timestamp":
                        result = str(int(now.timestamp()))
                    else:  # readable
                        result = now.strftime("%Y-%m-%d %H:%M:%S")
                    
                    return [
                        types.TextContent(
                            type="text",
                            text=f"Current time ({format_type}): {result}"
                        )
                    ]
                except Exception as e:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"Error getting time: {str(e)}"
                        )
                    ]
            
            else:
                return [
                    types.TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )
                ]
        
        # Resource handlers
        @self.server.list_resources()
        async def handle_list_resources() -> List[types.Resource]:
            """List available resources."""
            return [
                types.Resource(
                    uri=AnyUrl("basic://system_info"),
                    name="System Information",
                    description="Basic system and environment information",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri=AnyUrl("basic://server_config"),
                    name="Server Configuration",
                    description="Basic server configuration and capabilities",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri=AnyUrl("basic://help"),
                    name="Help Documentation",
                    description="Basic usage instructions and examples",
                    mimeType="text/plain"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            """Handle resource reading."""
            
            if str(uri) == "basic://system_info":
                system_info = {
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "hostname": platform.node(),
                    "processor": platform.processor(),
                    "python_version": sys.version,
                    "current_working_directory": os.getcwd(),
                    "environment_variables_count": len(os.environ),
                    "timestamp": datetime.now().isoformat()
                }
                return json.dumps(system_info, indent=2)
            
            elif str(uri) == "basic://server_config":
                config = {
                    "server_name": "basic-mcp-server",
                    "version": "1.0.0",
                    "capabilities": {
                        "tools": ["calculator", "string_utils", "get_current_time"],
                        "resources": ["system_info", "server_config", "help"],
                        "prompts": ["calculation_helper", "text_processing"]
                    },
                    "description": "A basic MCP server for learning and demonstration",
                    "author": "MCP Learning Project",
                    "created": datetime.now().isoformat()
                }
                return json.dumps(config, indent=2)
            
            elif str(uri) == "basic://help":
                help_text = """
# Basic MCP Server Help

## Available Tools:

1. **calculator**
   - Description: Perform basic mathematical calculations
   - Usage: Provide a mathematical expression as a string
   - Example: "2 + 3 * 4" → Result: 14

2. **string_utils**
   - Description: String manipulation utilities
   - Operations: uppercase, lowercase, reverse, length, words
   - Example: text="Hello World", operation="uppercase" → "HELLO WORLD"

3. **get_current_time**
   - Description: Get current date and time
   - Formats: iso, readable, timestamp
   - Example: format="readable" → "2025-08-25 15:30:45"

## Available Resources:

1. **system_info** - System and environment information
2. **server_config** - Server configuration and capabilities
3. **help** - This help documentation

## Available Prompts:

1. **calculation_helper** - Assists with mathematical calculations
2. **text_processing** - Helps with text manipulation tasks

## Usage Examples:

```json
// Calculator tool call
{
  "tool": "calculator",
  "arguments": {
    "expression": "10 + 5 * 2"
  }
}

// String utils tool call
{
  "tool": "string_utils", 
  "arguments": {
    "text": "Hello MCP World",
    "operation": "uppercase"
  }
}
```

For more information, see the project documentation.
                """
                return help_text.strip()
            
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        # Prompt handlers
        @self.server.list_prompts()
        async def handle_list_prompts() -> List[types.Prompt]:
            """List available prompts."""
            return [
                types.Prompt(
                    name="calculation_helper",
                    description="Helps with mathematical calculations and explanations",
                    arguments=[
                        types.PromptArgument(
                            name="problem",
                            description="Mathematical problem to solve",
                            required=True
                        )
                    ]
                ),
                types.Prompt(
                    name="text_processing",
                    description="Assists with text manipulation and analysis",
                    arguments=[
                        types.PromptArgument(
                            name="text",
                            description="Text to process",
                            required=True
                        ),
                        types.PromptArgument(
                            name="task",
                            description="Processing task to perform",
                            required=False
                        )
                    ]
                )
            ]
        
        @self.server.get_prompt()
        async def handle_get_prompt(
            name: str, arguments: Dict[str, str]
        ) -> types.GetPromptResult:
            """Handle prompt generation."""
            
            if name == "calculation_helper":
                problem = arguments.get("problem", "")
                prompt_text = f"""
You are a helpful mathematical assistant. Help solve this problem step by step:

Problem: {problem}

Please:
1. Break down the problem into clear steps
2. Show your work for each step
3. Provide the final answer
4. Explain the mathematical concepts involved

Available tools:
- calculator: Use this for any numerical calculations
- You can use the calculator tool multiple times for complex problems

Remember to be clear and educational in your explanations.
                """
                
                return types.GetPromptResult(
                    description=f"Mathematical problem solving assistance for: {problem}",
                    messages=[
                        types.PromptMessage(
                            role="user",
                            content=types.TextContent(
                                type="text",
                                text=prompt_text.strip()
                            )
                        )
                    ]
                )
            
            elif name == "text_processing":
                text = arguments.get("text", "")
                task = arguments.get("task", "general analysis")
                
                prompt_text = f"""
You are a helpful text processing assistant. Process the following text:

Text: {text}
Task: {task}

Please use the available string utilities tools to:
1. Analyze the text (length, word count, etc.)
2. Apply appropriate transformations based on the task
3. Provide insights about the text structure and content

Available tools:
- string_utils: Can perform operations like uppercase, lowercase, reverse, length, words

Be thorough in your analysis and provide useful insights.
                """
                
                return types.GetPromptResult(
                    description=f"Text processing assistance for: {task}",
                    messages=[
                        types.PromptMessage(
                            role="user",
                            content=types.TextContent(
                                type="text",
                                text=prompt_text.strip()
                            )
                        )
                    ]
                )
            
            else:
                raise ValueError(f"Unknown prompt: {name}")
    
    async def run(self):
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                NotificationOptions(
                    prompts_changed=True,
                    resources_changed=True,
                    tools_changed=True,
                ),
            )


def main():
    """Main entry point for the server."""
    print("Starting Basic MCP Server...", file=sys.stderr)
    print("This server provides basic tools, resources, and prompts.", file=sys.stderr)
    print("Connect using an MCP client to interact with the server.", file=sys.stderr)
    
    server = BasicMCPServer()
    asyncio.run(server.run())


# Export the class for importing
__all__ = ["BasicMCPServer"]


if __name__ == "__main__":
    main()