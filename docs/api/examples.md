# MCP Examples and Usage Scenarios

## Basic Examples

### 1. Simple Calculator Tool
```python
# Connect to basic server and use calculator
result = await client.call_tool("calculator", {
    "expression": "10 + 5 * 2"
})
# Output: Result: 20
```

### 2. String Processing
```python
# Text manipulation examples
await client.call_tool("string_utils", {
    "text": "Hello MCP World",
    "operation": "uppercase"
})
# Output: HELLO MCP WORLD

await client.call_tool("string_utils", {
    "text": "Data Analysis",
    "operation": "reverse"
})
# Output: sisylanA ataD
```

## Data Analysis Examples

### 1. Complete Data Analysis Workflow
```python
# Load dataset
await client.call_tool("load_dataset", {
    "path": "data/sample_data.csv",
    "name": "employees"
})

# Get overview
info = await client.call_tool("dataset_info", {"name": "employees"})

# Statistical analysis
stats = await client.call_tool("calculate_statistics", {"name": "employees"})

# Find relationships
corr = await client.call_tool("find_correlations", {
    "name": "employees",
    "threshold": 0.3
})

# Group analysis
groups = await client.call_tool("group_analysis", {
    "name": "employees", 
    "group_by": "department",
    "agg_columns": ["salary", "age"]
})
```

### 2. Data Quality Assessment
```python
# Comprehensive quality check
quality = await client.call_tool("data_quality_check", {"name": "employees"})

# Generate insights
insights = await client.call_tool("generate_insights", {
    "name": "employees",
    "focus": "recommendations"
})
```

## File Operations Examples

### 1. File Management
```python
# Read file
content = await client.call_tool("file_read", {
    "path": "data/config.txt"
})

# Write file
await client.call_tool("file_write", {
    "path": "output/results.txt",
    "content": "Analysis complete"
})

# List directory
files = await client.call_tool("directory_list", {
    "path": "data/",
    "show_hidden": False
})
```

## Real-World Scenarios

### Scenario 1: Sales Data Analysis
Perfect for business analysts examining sales performance.

```python
# Load quarterly sales data
await client.call_tool("load_dataset", {
    "path": "sales_q4_2024.csv", 
    "name": "sales"
})

# Check data quality
quality = await client.call_tool("data_quality_check", {"name": "sales"})

# Sales by region analysis
regional = await client.call_tool("group_analysis", {
    "name": "sales",
    "group_by": "region", 
    "agg_columns": ["revenue", "units_sold"],
    "operations": ["sum", "mean", "count"]
})

# Find product correlations
products = await client.call_tool("find_correlations", {
    "name": "sales",
    "threshold": 0.4
})
```

### Scenario 2: HR Analytics
Analyzing employee data for HR insights.

```python
# Load employee dataset
await client.call_tool("load_dataset", {
    "path": "hr_data.csv",
    "name": "hr"
})

# Department performance analysis
dept_stats = await client.call_tool("group_analysis", {
    "name": "hr",
    "group_by": "department",
    "agg_columns": ["salary", "performance_score", "experience_years"]
})

# Salary correlation analysis
salary_corr = await client.call_tool("find_correlations", {
    "name": "hr", 
    "threshold": 0.3
})

# Get actionable insights
hr_insights = await client.call_tool("generate_insights", {
    "name": "hr",
    "focus": "patterns"
})
```

## Integration Examples

### 1. Automated Reporting
```python
async def generate_weekly_report():
    client = MCPClientExample()
    await client.connect_to_server(["python", "src/mcp_servers/data_analysis_server.py"])
    
    # Load this week's data
    await client.call_tool("load_dataset", {
        "path": "weekly_metrics.csv",
        "name": "weekly"
    })
    
    # Generate statistics
    stats = await client.call_tool("calculate_statistics", {"name": "weekly"})
    
    # Create report
    await client.call_tool("file_write", {
        "path": f"reports/week_{datetime.now().strftime('%Y%m%d')}.txt",
        "content": f"Weekly Report\n{stats}"
    })
    
    await client.disconnect()
```

### 2. Data Pipeline
```python
async def process_data_pipeline():
    # Process multiple datasets
    datasets = ["customers.csv", "orders.csv", "products.csv"]
    
    for dataset in datasets:
        await client.call_tool("load_dataset", {
            "path": f"raw_data/{dataset}",
            "name": dataset.replace('.csv', '')
        })
        
        # Quality check each dataset
        quality = await client.call_tool("data_quality_check", {
            "name": dataset.replace('.csv', '')
        })
        
        print(f"Processed {dataset}: {quality}")
```

## Best Practices

### 1. Error Handling
```python
try:
    result = await client.call_tool("calculator", {"expression": "invalid"})
except Exception as e:
    print(f"Tool execution failed: {e}")
```

### 2. Resource Management
```python
async def safe_client_usage():
    client = MCPClientExample()
    try:
        await client.connect_to_server(server_command)
        # Your work here
        result = await client.call_tool("tool_name", args)
    finally:
        await client.disconnect()  # Always disconnect
```

### 3. Batch Processing
```python
# Process multiple files efficiently
files = ["data1.csv", "data2.csv", "data3.csv"]
for i, file in enumerate(files):
    await client.call_tool("load_dataset", {
        "path": file,
        "name": f"dataset_{i}"
    })
    
    stats = await client.call_tool("calculate_statistics", {
        "name": f"dataset_{i}"
    })
```