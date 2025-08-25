# MCP Data Analysis Toolkit API Reference

This document provides detailed API documentation for all MCP servers and clients in the MCP Data Analysis Toolkit.

## Basic MCP Server (`src/mcp_servers/basic_server.py`)

### Overview
Simple MCP server demonstrating core MCP concepts with basic tools and resources.

### Tools

#### `calculator`
Performs basic mathematical calculations.

**Parameters:**
- `expression` (string, required): Mathematical expression to evaluate

**Example:**
```json
{
  "tool": "calculator",
  "arguments": {
    "expression": "10 + 5 * 2"
  }
}
```

**Response:**
```
Result: 20
Expression: 10 + 5 * 2
```

#### `string_utils`
String manipulation utilities.

**Parameters:**
- `text` (string, required): Text to manipulate
- `operation` (string, required): One of "uppercase", "lowercase", "reverse", "length", "words"

**Example:**
```json
{
  "tool": "string_utils",
  "arguments": {
    "text": "Hello MCP",
    "operation": "uppercase"
  }
}
```

#### `get_current_time`
Get current date and time in various formats.

**Parameters:**
- `format` (string, optional): "iso", "readable", or "timestamp". Default: "readable"

### Resources

#### `basic://system_info`
Returns system and environment information as JSON.

**Content:**
- Platform information
- Python version
- Current working directory
- Environment variables count

#### `basic://server_config`
Returns server configuration and capabilities as JSON.

#### `basic://help`
Returns comprehensive help documentation as plain text.

### Prompts

#### `calculation_helper`
Assists with mathematical problem solving.

**Arguments:**
- `problem` (string, required): Mathematical problem to solve

#### `text_processing`
Helps with text manipulation tasks.

**Arguments:**
- `text` (string, required): Text to process
- `task` (string, optional): Processing task description

---

## Advanced MCP Server (`src/mcp_servers/advanced_server.py`)

### Overview
Advanced MCP server with file operations and enhanced data processing capabilities.

### Tools

#### `file_read`
Read contents of a file.

**Parameters:**
- `path` (string, required): File path to read
- `encoding` (string, optional): File encoding. Default: "utf-8"

**Security Note:** Server validates file paths and restricts access to safe locations.

#### `file_write`
Write content to a file.

**Parameters:**
- `path` (string, required): File path to write
- `content` (string, required): Content to write
- `encoding` (string, optional): File encoding. Default: "utf-8"

#### `directory_list`
List directory contents.

**Parameters:**
- `path` (string, required): Directory path to list
- `show_hidden` (boolean, optional): Include hidden files. Default: false

#### `csv_analyze` (requires pandas)
Analyze CSV file and provide comprehensive statistics.

**Parameters:**
- `path` (string, required): CSV file path
- `delimiter` (string, optional): CSV delimiter. Default: ","

**Returns:**
- File information
- Data shape and structure
- Column types and statistics
- Null value analysis

#### `data_summary` (requires pandas)
Generate detailed summary statistics for datasets.

**Parameters:**
- `path` (string, required): Data file path
- `columns` (array, optional): Specific columns to analyze

### Resources

#### `advanced://capabilities`
Returns server capabilities and feature information as JSON.

#### `advanced://temp_workspace`
Information about the temporary workspace directory.

---

## Data Analysis MCP Server (`src/mcp_servers/data_analysis_server.py`)

### Overview
Specialized server for comprehensive data analysis, perfect for data analysts and researchers.

### Tools

#### `load_dataset`
Load a dataset from file into memory for analysis.

**Parameters:**
- `path` (string, required): Path to dataset file (CSV or JSON)
- `name` (string, required): Name to reference this dataset
- `delimiter` (string, optional): CSV delimiter. Default: ","

**Example:**
```json
{
  "tool": "load_dataset",
  "arguments": {
    "path": "data/sales.csv",
    "name": "sales_data"
  }
}
```

#### `dataset_info`
Get comprehensive information about a loaded dataset.

**Parameters:**
- `name` (string, required): Dataset name

**Returns:**
- Dataset shape (rows, columns)
- Column names and data types
- Null value counts
- Unique value counts
- Sample data rows
- Memory usage information

#### `calculate_statistics`
Calculate descriptive statistics for numeric columns.

**Parameters:**
- `name` (string, required): Dataset name
- `columns` (array, optional): Specific columns to analyze
- `include_percentiles` (boolean, optional): Include percentile statistics. Default: true

**Returns:**
- Count, mean, std, min, max
- Quartiles (25%, 50%, 75%)
- Additional percentiles (90%, 95%) if requested

#### `find_correlations`
Discover correlations between numeric variables.

**Parameters:**
- `name` (string, required): Dataset name
- `method` (string, optional): "pearson", "spearman", or "kendall". Default: "pearson"
- `threshold` (number, optional): Minimum correlation threshold. Default: 0.5

**Returns:**
- High correlation pairs above threshold
- Correlation strength classification
- Full correlation matrix

#### `group_analysis`
Perform group-by analysis on dataset.

**Parameters:**
- `name` (string, required): Dataset name
- `group_by` (string, required): Column to group by
- `agg_columns` (array, optional): Columns to aggregate
- `operations` (array, optional): Aggregation operations. Default: ["mean", "count"]

**Example:**
```json
{
  "tool": "group_analysis",
  "arguments": {
    "name": "employees",
    "group_by": "department",
    "agg_columns": ["salary", "age"],
    "operations": ["mean", "median", "count"]
  }
}
```

#### `data_quality_check`
Comprehensive data quality assessment.

**Parameters:**
- `name` (string, required): Dataset name

**Returns:**
- Missing data analysis
- Duplicate row detection
- Data type consistency
- Unique value analysis
- Potential data issues identification

#### `generate_insights`
Generate automated insights and recommendations.

**Parameters:**
- `name` (string, required): Dataset name
- `focus` (string, optional): "overview", "outliers", "patterns", or "recommendations". Default: "overview"

**Returns:**
- Automated analysis insights
- Pattern detection
- Outlier identification
- Actionable recommendations

### Resources

#### `data://loaded_datasets`
Information about all currently loaded datasets.

**Content:**
- Dataset names and metadata
- Memory usage information
- Column information for each dataset

#### `data://analysis_guide`
Comprehensive guide for performing data analysis.

**Content:**
- Step-by-step analysis workflow
- Best practices for data analysts
- Tool usage examples
- Statistical interpretation guidelines

#### `data://dataset/{name}`
Detailed information about a specific loaded dataset.

**Content:**
- Complete dataset metadata
- Sample data preview
- Statistical summaries
- Data quality metrics

---

## MCP Client (`client_example.py`)

### Overview
Comprehensive MCP client demonstrating how to connect to and interact with MCP servers.

### Class: `MCPClientExample`

#### Methods

##### `connect_to_server(server_command: List[str]) -> bool`
Connect to an MCP server using stdio transport.

**Parameters:**
- `server_command`: Command to start the server process

**Returns:**
- `True` if connection successful, `False` otherwise

##### `disconnect()`
Disconnect from the current server and clean up resources.

##### `list_tools() -> List[types.Tool]`
List all available tools from the connected server.

##### `call_tool(name: str, arguments: Dict[str, Any]) -> Any`
Execute a tool on the server.

**Parameters:**
- `name`: Tool name
- `arguments`: Tool arguments as dictionary

##### `list_resources() -> List[types.Resource]`
List all available resources from the server.

##### `read_resource(uri: str) -> str`
Read content from a specific resource.

##### `list_prompts() -> List[types.Prompt]`
List all available prompts from the server.

##### `get_prompt(name: str, arguments: Dict[str, str]) -> Any`
Get a specific prompt with arguments.

### Usage Examples

#### Basic Connection and Tool Usage

```python
import asyncio
from client_example import MCPClientExample

async def example():
    client = MCPClientExample()
    
    # Connect to server
    await client.connect_to_server(["python", "examples/basic_server.py"])
    
    # List available tools
    tools = await client.list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Call a tool
    result = await client.call_tool("calculator", {"expression": "5 + 3"})
    print(f"Calculator result: {result}")
    
    # Disconnect
    await client.disconnect()

asyncio.run(example())
```

#### Data Analysis Workflow

```python
async def data_analysis_example():
    client = MCPClientExample()
    await client.connect_to_server(["python", "examples/data_analysis_server.py"])
    
    # Load dataset
    await client.call_tool("load_dataset", {
        "path": "data/sample_data.csv",
        "name": "employees"
    })
    
    # Get dataset information
    info = await client.call_tool("dataset_info", {"name": "employees"})
    
    # Calculate statistics
    stats = await client.call_tool("calculate_statistics", {"name": "employees"})
    
    # Find correlations
    corr = await client.call_tool("find_correlations", {
        "name": "employees",
        "threshold": 0.3
    })
    
    await client.disconnect()
```

---

## Configuration (`config/server_config.json`)

### Structure

The configuration file defines server configurations and capabilities:

```json
{
  "servers": {
    "server-name": {
      "name": "Display Name",
      "description": "Server description",
      "command": ["python", "path/to/server.py"],
      "capabilities": {
        "tools": ["tool1", "tool2"],
        "resources": ["resource1", "resource2"],
        "prompts": ["prompt1", "prompt2"]
      },
      "dependencies": ["pandas", "numpy"],
      "recommended_for": ["use_case1", "use_case2"]
    }
  }
}
```

### Server Configurations

#### Basic Server
- **Command:** `["python", "examples/basic_server.py"]`
- **Tools:** calculator, string_utils, get_current_time
- **Best for:** Learning MCP concepts, simple automation

#### Advanced Server
- **Command:** `["python", "examples/advanced_server.py"]`
- **Tools:** file_read, file_write, directory_list, csv_analyze
- **Dependencies:** pandas (optional)
- **Best for:** File management, data processing

#### Data Analysis Server
- **Command:** `["python", "examples/data_analysis_server.py"]`
- **Tools:** Full data analysis suite
- **Dependencies:** pandas, numpy
- **Best for:** Statistical analysis, business intelligence

---

## Error Handling

### Common Error Patterns

#### Tool Execution Errors
```json
{
  "error": "Error message describing what went wrong",
  "tool": "tool_name",
  "arguments": {...}
}
```

#### Resource Access Errors
```json
{
  "error": "Resource not found or access denied",
  "resource": "resource_uri"
}
```

#### Connection Errors
- Server process fails to start
- Communication timeout
- Protocol version mismatch

### Best Practices

1. **Always check connection status** before calling tools
2. **Handle exceptions gracefully** in tool implementations
3. **Validate input parameters** before processing
4. **Provide meaningful error messages** to help debugging
5. **Clean up resources** when disconnecting

---

## Performance Considerations

### Memory Usage
- Data analysis server caches loaded datasets in memory
- Large datasets may require significant RAM
- Consider using chunked processing for very large files

### Processing Speed
- File operations are I/O bound
- Statistical calculations depend on dataset size
- Use appropriate data types for optimal performance

### Scalability
- Current examples use stdio transport (single-process)
- For production, consider HTTP transport for multi-client support
- Implement connection pooling for high-traffic scenarios

---

## Security Notes

### File Access
- Advanced server restricts file access to safe locations
- Validate all file paths to prevent directory traversal
- Consider implementing additional access controls

### Code Execution
- Calculator tool uses eval() with basic safety checks
- For production, implement proper expression parsing
- Never execute untrusted code without sandboxing

### Data Privacy
- Datasets loaded into memory are cached until server restart
- Consider data encryption for sensitive information
- Implement proper access logging and audit trails