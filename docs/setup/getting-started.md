# Getting Started with MCP Data Analysis Toolkit

This guide will help you understand and work with Model Context Protocol (MCP) using our comprehensive data analysis toolkit.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or download the project** to your local machine

2. **Install dependencies**:
   ```bash
   cd mcp-data-analysis-toolkit
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -c "import mcp; print('MCP installed successfully')"
   ```

## Understanding MCP

**Model Context Protocol (MCP)** is an open standard that enables AI applications to securely connect with external data sources and tools. Think of it as a universal translator between AI systems and your data.

### Key Components:

- **MCP Server**: Provides tools, resources, and prompts to AI applications
- **MCP Client**: Connects to servers and facilitates communication
- **Tools**: Functions that AI can execute (like calculations, file operations)
- **Resources**: Data sources that provide context (like files, databases)
- **Prompts**: Templates that help structure AI interactions

## Quick Start Examples

### 1. Basic Server Demo

Start with the simplest example:

```bash
# Terminal 1: Start the basic server
python src/mcp_servers/basic_server.py

# Terminal 2: Run the client demo
python src/clients/client_example.py basic
```

This demonstrates:
- Basic tools (calculator, string utilities, time)
- Simple resources (system info, configuration)
- Prompt templates for AI interactions

### 2. Data Analysis Demo

Perfect for data analysts:

```bash
# Run the data analysis demo
python src/clients/client_example.py data
```

This shows:
- Loading and analyzing datasets
- Statistical calculations
- Correlation analysis
- Data quality assessment
- Automated insights generation

### 3. Interactive Client

Explore MCP interactively:

```bash
python src/clients/client_example.py interactive
```

This allows you to:
- Choose between different servers
- Explore available tools and resources
- Execute tools with custom parameters
- Read resources and understand their content

## Step-by-Step Tutorial

### Step 1: Understanding the Basic Server

1. **Start the basic server**:
   ```bash
   python src/mcp_servers/basic_server.py
   ```

2. **In another terminal, explore its capabilities**:
   ```bash
   python src/clients/client_example.py basic
   ```

3. **Observe the output** to understand:
   - How tools are listed and called
   - How resources provide contextual information
   - How prompts structure AI interactions

### Step 2: Working with Data Analysis

1. **Examine the sample data**:
   ```bash
   # Look at the sample dataset
   type data\sample_data.csv  # Windows
   # or
   cat data/sample_data.csv   # macOS/Linux
   ```

2. **Run data analysis**:
   ```bash
   python src/clients/client_example.py data
   ```

3. **Study the analysis output**:
   - Dataset loading and basic information
   - Statistical summaries
   - Correlation patterns
   - Data quality insights

### Step 3: Building Your Own Server

Create a simple custom server:

```python
#!/usr/bin/env python3
import asyncio
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

class MyCustomServer:
    def __init__(self):
        self.server = Server("my-custom-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools():
            return [
                types.Tool(
                    name="greet",
                    description="Generate a personalized greeting",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Name to greet"}
                        },
                        "required": ["name"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            if name == "greet":
                name_arg = arguments.get("name", "World")
                return [types.TextContent(
                    type="text",
                    text=f"Hello, {name_arg}! Welcome to MCP!"
                )]

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, 
                               mcp.server.NotificationOptions())

if __name__ == "__main__":
    server = MyCustomServer()
    asyncio.run(server.run())
```

## Common Use Cases

### For Data Analysts

Use the data analysis server to:
- Load CSV files and get instant insights
- Perform correlation analysis on your datasets
- Generate statistical summaries
- Identify data quality issues
- Get automated recommendations for analysis

Example workflow:
```bash
# Start data analysis server
python src/mcp_servers/data_analysis_server.py

# In client, load your data
load_dataset(path="your_data.csv", name="analysis")
dataset_info(name="analysis")
calculate_statistics(name="analysis")
find_correlations(name="analysis", threshold=0.5)
```

### For Developers

Use MCP to:
- Create tools that AI can use to interact with your APIs
- Provide contextual information through resources
- Build AI-powered automation workflows
- Integrate AI capabilities into existing systems

### For System Administrators

Use MCP to:
- Create monitoring and management tools
- Provide system information to AI assistants
- Automate routine tasks through AI interactions
- Build diagnostic and troubleshooting tools

## Advanced Features

### Custom Transport

While our examples use stdio transport, MCP also supports HTTP transport for remote servers:

```python
# Example HTTP transport (not fully implemented in examples)
# This would allow remote MCP servers
async def http_server_example():
    # Implementation would use HTTP transport
    # instead of stdio for remote access
    pass
```

### Resource Subscriptions

MCP supports dynamic resources that can change over time:

```python
@server.list_resources()
async def dynamic_resources():
    # Resources can be generated dynamically
    # based on current system state
    return resources_based_on_current_state()
```

### Tool Chaining

Tools can call other tools, creating powerful workflows:

```python
async def complex_tool(arguments):
    # Call multiple tools in sequence
    result1 = await call_tool("tool1", args1)
    result2 = await call_tool("tool2", result1)
    return combine_results(result1, result2)
```

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Server Won't Start**: Check Python path and permissions
   ```bash
   python --version  # Should be 3.8+
   ```

3. **Client Connection Issues**: Ensure server is running before starting client

4. **Pandas Not Found**: Install data analysis dependencies
   ```bash
   pip install pandas numpy
   ```

### Debug Mode

Run servers with debug output:
```bash
python examples/basic_server.py 2>debug.log
```

## Next Steps

1. **Explore the codebase**: Study the server implementations to understand MCP patterns
2. **Modify examples**: Adapt the servers to your specific needs
3. **Build custom tools**: Create tools that interact with your systems
4. **Integrate with AI**: Connect your MCP servers to AI applications
5. **Scale up**: Deploy MCP servers for production use

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic MCP Documentation](https://www.anthropic.com/news/model-context-protocol)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Community Examples](https://github.com/modelcontextprotocol/servers)

## Support

For questions and issues:
1. Check the troubleshooting section above
2. Review the example code and comments
3. Consult the official MCP documentation
4. Join the MCP community discussions

Happy coding with MCP! 🚀