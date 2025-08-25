#!/usr/bin/env python3
"""
MCP Client Example

Demonstrates how to create an MCP client that connects to MCP servers
and interacts with their tools, resources, and prompts.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

import mcp.client.stdio
import mcp.types as types
from mcp.client.session import ClientSession


class MCPClientExample:
    """Example MCP client for interacting with MCP servers."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.server_process: Optional[subprocess.Popen] = None
    
    async def connect_to_server(self, server_command: List[str]) -> bool:
        """Connect to an MCP server using stdio transport."""
        try:
            print(f"Starting server: {' '.join(server_command)}")
            
            # Start the server process
            self.server_process = subprocess.Popen(
                server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Create stdio connection
            async with mcp.client.stdio.stdio_client(
                self.server_process.stdout, 
                self.server_process.stdin
            ) as (read_stream, write_stream):
                
                # Initialize client session
                self.session = ClientSession(read_stream, write_stream)
                
                # Initialize the connection
                init_result = await self.session.initialize()
                print(f"Connected to server: {init_result.server_info.name}")
                print(f"Server version: {init_result.server_info.version}")
                
                return True
            
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            await self.disconnect()
            return False
    
    async def disconnect(self):
        """Disconnect from the server."""
        if self.session:
            await self.session.close()
            self.session = None
        
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
        
        print("Disconnected from server")
    
    async def list_tools(self) -> List[types.Tool]:
        """List available tools from the server."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        result = await self.session.list_tools()
        return result.tools
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the server."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        result = await self.session.call_tool(name, arguments)
        return result.content
    
    async def list_resources(self) -> List[types.Resource]:
        """List available resources from the server."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        result = await self.session.list_resources()
        return result.resources
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource from the server."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        result = await self.session.read_resource(uri)
        return result.contents[0].text if result.contents else ""
    
    async def list_prompts(self) -> List[types.Prompt]:
        """List available prompts from the server."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        result = await self.session.list_prompts()
        return result.prompts
    
    async def get_prompt(self, name: str, arguments: Dict[str, str]) -> Any:
        """Get a prompt from the server."""
        if not self.session:
            raise RuntimeError("Not connected to server")
        
        result = await self.session.get_prompt(name, arguments)
        return result
    
    async def demonstrate_basic_server(self):
        """Demonstrate interaction with the basic MCP server."""
        print("\n" + "="*60)
        print("DEMONSTRATING BASIC MCP SERVER")
        print("="*60)
        
        # Connect to basic server
        server_cmd = [sys.executable, "src/mcp_servers/basic_server.py"]
        if not await self.connect_to_server(server_cmd):
            return
        
        try:
            # List and test tools
            print("\n📧 LISTING TOOLS:")
            tools = await self.list_tools()
            for tool in tools:
                print(f"• {tool.name}: {tool.description}")
            
            print("\n🔧 TESTING TOOLS:")
            
            # Test calculator
            print("\n1. Calculator Tool:")
            result = await self.call_tool("calculator", {"expression": "10 + 5 * 2"})
            print(f"   Result: {result[0].text}")
            
            # Test string utils
            print("\n2. String Utils Tool:")
            result = await self.call_tool("string_utils", {
                "text": "Hello MCP World", 
                "operation": "uppercase"
            })
            print(f"   Result: {result[0].text}")
            
            # Test time tool
            print("\n3. Current Time Tool:")
            result = await self.call_tool("get_current_time", {"format": "readable"})
            print(f"   Result: {result[0].text}")
            
            # List and read resources
            print("\n📚 RESOURCES:")
            resources = await self.list_resources()
            for resource in resources:
                print(f"\n• {resource.name}:")
                content = await self.read_resource(str(resource.uri))
                if resource.mimeType == "application/json":
                    data = json.loads(content)
                    print(f"   {json.dumps(data, indent=4)[:200]}...")
                else:
                    print(f"   {content[:200]}...")
            
            # List prompts
            print("\n💬 PROMPTS:")
            prompts = await self.list_prompts()
            for prompt in prompts:
                print(f"• {prompt.name}: {prompt.description}")
            
        finally:
            await self.disconnect()
    
    async def demonstrate_data_analysis_server(self):
        """Demonstrate interaction with the data analysis server."""
        print("\n" + "="*60)
        print("DEMONSTRATING DATA ANALYSIS SERVER")
        print("="*60)
        
        # Connect to data analysis server
        server_cmd = [sys.executable, "src/mcp_servers/data_analysis_server.py"]
        if not await self.connect_to_server(server_cmd):
            return
        
        try:
            # List tools
            print("\n📊 DATA ANALYSIS TOOLS:")
            tools = await self.list_tools()
            for tool in tools:
                print(f"• {tool.name}: {tool.description}")
            
            print("\n🔍 TESTING DATA ANALYSIS:")
            
            # Load sample dataset
            print("\n1. Loading Sample Dataset:")
            result = await self.call_tool("load_dataset", {
                "path": "data/sample_data.csv",
                "name": "employees"
            })
            print(f"   {result[0].text}")
            
            # Get dataset info
            print("\n2. Dataset Information:")
            result = await self.call_tool("dataset_info", {"name": "employees"})
            data = json.loads(result[0].text.split("Dataset Information:\n")[1])
            print(f"   Shape: {data['shape']}")
            print(f"   Columns: {data['columns']['names']}")
            
            # Calculate statistics
            print("\n3. Statistical Analysis:")
            result = await self.call_tool("calculate_statistics", {"name": "employees"})
            stats_lines = result[0].text.split('\n')[:10]  # Show first 10 lines
            print("   " + "\n   ".join(stats_lines))
            
            # Find correlations
            print("\n4. Correlation Analysis:")
            result = await self.call_tool("find_correlations", {
                "name": "employees",
                "threshold": 0.3
            })
            corr_lines = result[0].text.split('\n')[:15]  # Show first 15 lines
            print("   " + "\n   ".join(corr_lines))
            
            # Group analysis
            print("\n5. Group Analysis by Department:")
            result = await self.call_tool("group_analysis", {
                "name": "employees",
                "group_by": "department",
                "agg_columns": ["salary", "age"],
                "operations": ["mean", "count"]
            })
            group_lines = result[0].text.split('\n')[:10]  # Show first 10 lines
            print("   " + "\n   ".join(group_lines))
            
            # Data quality check
            print("\n6. Data Quality Assessment:")
            result = await self.call_tool("data_quality_check", {"name": "employees"})
            quality_data = json.loads(result[0].text.split("Data Quality Report:\n")[1])
            print(f"   Total rows: {quality_data['total_rows']}")
            print(f"   Missing values: {quality_data['missing_data']['total_missing_values']}")
            print(f"   Duplicate rows: {quality_data['duplicates']['duplicate_rows']}")
            
            # Generate insights
            print("\n7. Automated Insights:")
            result = await self.call_tool("generate_insights", {
                "name": "employees",
                "focus": "recommendations"
            })
            insights_lines = result[0].text.split('\n')[:15]  # Show first 15 lines
            print("   " + "\n   ".join(insights_lines))
            
        finally:
            await self.disconnect()
    
    async def demonstrate_interactive_session(self):
        """Run an interactive session with user input."""
        print("\n" + "="*60)
        print("INTERACTIVE MCP CLIENT SESSION")
        print("="*60)
        print("Available servers:")
        print("1. Basic Server (basic tools and utilities)")
        print("2. Data Analysis Server (data analysis tools)")
        print("3. Exit")
        
        while True:
            try:
                choice = input("\nSelect server (1-3): ").strip()
                
                if choice == "3":
                    break
                elif choice == "1":
                    server_cmd = [sys.executable, "src/mcp_servers/basic_server.py"]
                    server_name = "Basic Server"
                elif choice == "2":
                    server_cmd = [sys.executable, "src/mcp_servers/data_analysis_server.py"]
                    server_name = "Data Analysis Server"
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
                    continue
                
                print(f"\nConnecting to {server_name}...")
                if not await self.connect_to_server(server_cmd):
                    continue
                
                await self.interactive_session_loop()
                await self.disconnect()
                
            except KeyboardInterrupt:
                print("\nSession interrupted by user.")
                await self.disconnect()
                break
            except Exception as e:
                print(f"Error in interactive session: {e}")
                await self.disconnect()
    
    async def interactive_session_loop(self):
        """Main loop for interactive session."""
        while True:
            print("\nCommands:")
            print("1. List tools")
            print("2. Call tool")
            print("3. List resources")
            print("4. Read resource")
            print("5. List prompts")
            print("6. Back to server selection")
            
            try:
                cmd = input("\nEnter command (1-6): ").strip()
                
                if cmd == "6":
                    break
                elif cmd == "1":
                    tools = await self.list_tools()
                    print("\nAvailable tools:")
                    for i, tool in enumerate(tools, 1):
                        print(f"{i}. {tool.name}: {tool.description}")
                
                elif cmd == "2":
                    tools = await self.list_tools()
                    print("\nAvailable tools:")
                    for i, tool in enumerate(tools, 1):
                        print(f"{i}. {tool.name}")
                    
                    tool_idx = int(input("Select tool number: ")) - 1
                    if 0 <= tool_idx < len(tools):
                        tool = tools[tool_idx]
                        print(f"\nCalling {tool.name}")
                        print(f"Schema: {json.dumps(tool.inputSchema, indent=2)}")
                        
                        arguments = {}
                        # Simple argument collection (in real client, use proper JSON input)
                        if "properties" in tool.inputSchema:
                            for prop, details in tool.inputSchema["properties"].items():
                                if prop in tool.inputSchema.get("required", []):
                                    value = input(f"Enter {prop} ({details.get('description', '')}): ")
                                    arguments[prop] = value
                        
                        result = await self.call_tool(tool.name, arguments)
                        print(f"\nResult: {result[0].text}")
                
                elif cmd == "3":
                    resources = await self.list_resources()
                    print("\nAvailable resources:")
                    for i, resource in enumerate(resources, 1):
                        print(f"{i}. {resource.name}: {resource.description}")
                
                elif cmd == "4":
                    resources = await self.list_resources()
                    print("\nAvailable resources:")
                    for i, resource in enumerate(resources, 1):
                        print(f"{i}. {resource.name}")
                    
                    res_idx = int(input("Select resource number: ")) - 1
                    if 0 <= res_idx < len(resources):
                        resource = resources[res_idx]
                        content = await self.read_resource(str(resource.uri))
                        print(f"\nResource content:\n{content[:500]}...")
                
                elif cmd == "5":
                    prompts = await self.list_prompts()
                    print("\nAvailable prompts:")
                    for i, prompt in enumerate(prompts, 1):
                        print(f"{i}. {prompt.name}: {prompt.description}")
                
                else:
                    print("Invalid command.")
                    
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
            except KeyboardInterrupt:
                print("\nReturning to main menu...")
                break


async def main():
    """Main function to run the client examples."""
    client = MCPClientExample()
    
    print("MCP Client Example")
    print("This client demonstrates connecting to and interacting with MCP servers.")
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "basic":
            await client.demonstrate_basic_server()
        elif mode == "data":
            await client.demonstrate_data_analysis_server()
        elif mode == "interactive":
            await client.demonstrate_interactive_session()
        else:
            print(f"Unknown mode: {mode}")
    else:
        print("\nRunning all demonstrations...")
        await client.demonstrate_basic_server()
        await client.demonstrate_data_analysis_server()
        
        print("\n" + "="*60)
        print("DEMONSTRATIONS COMPLETE")
        print("="*60)
        print("\nTo run interactive mode:")
        print("python src/clients/client_example.py interactive")


# Export the class for importing
__all__ = ["MCPClientExample"]


if __name__ == "__main__":
    asyncio.run(main())