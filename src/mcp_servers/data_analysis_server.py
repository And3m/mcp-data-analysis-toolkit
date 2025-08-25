#!/usr/bin/env python3
"""
Data Analysis MCP Server

Specialized MCP server for data analysts with:
- Advanced data processing capabilities
- Statistical analysis tools
- Data visualization preparation
- Dataset insights and recommendations
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None
    np = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('mcp_data_analysis.log')
    ]
)
logger = logging.getLogger(__name__)


class DataAnalysisMCPServer:
    """MCP server specialized for data analysis tasks."""
    
    def __init__(self):
        self.server = Server("data-analysis-mcp-server")
        self.datasets = {}  # Cache for loaded datasets
        self.analysis_history = []  # Track analysis operations
        logger.info("Initializing Data Analysis MCP Server")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up MCP handlers for data analysis."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available data analysis tools."""
            tools = [
                types.Tool(
                    name="load_dataset",
                    description="Load a dataset from file (CSV, JSON)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Path to dataset file"},
                            "name": {"type": "string", "description": "Name to reference this dataset"},
                            "delimiter": {"type": "string", "default": ",", "description": "CSV delimiter"}
                        },
                        "required": ["path", "name"]
                    }
                ),
                types.Tool(
                    name="dataset_info",
                    description="Get comprehensive information about a loaded dataset",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"}
                        },
                        "required": ["name"]
                    }
                ),
                types.Tool(
                    name="calculate_statistics",
                    description="Calculate descriptive statistics for dataset columns",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"},
                            "columns": {"type": "array", "items": {"type": "string"}, "description": "Specific columns (optional)"},
                            "include_percentiles": {"type": "boolean", "default": True}
                        },
                        "required": ["name"]
                    }
                ),
                types.Tool(
                    name="find_correlations",
                    description="Find correlations between numeric columns",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"},
                            "method": {"type": "string", "enum": ["pearson", "spearman", "kendall"], "default": "pearson"},
                            "threshold": {"type": "number", "default": 0.5, "description": "Minimum correlation threshold"}
                        },
                        "required": ["name"]
                    }
                ),
                types.Tool(
                    name="group_analysis",
                    description="Perform group-by analysis on dataset",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"},
                            "group_by": {"type": "string", "description": "Column to group by"},
                            "agg_columns": {"type": "array", "items": {"type": "string"}, "description": "Columns to aggregate"},
                            "operations": {"type": "array", "items": {"type": "string"}, "default": ["mean", "count"]}
                        },
                        "required": ["name", "group_by"]
                    }
                ),
                types.Tool(
                    name="data_quality_check",
                    description="Comprehensive data quality assessment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"}
                        },
                        "required": ["name"]
                    }
                ),
                types.Tool(
                    name="generate_insights",
                    description="Generate automated insights and recommendations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"},
                            "focus": {"type": "string", "enum": ["overview", "outliers", "patterns", "recommendations"], "default": "overview"}
                        },
                        "required": ["name"]
                    }
                ),
                types.Tool(
                    name="export_analysis",
                    description="Export analysis results to various formats",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"},
                            "format": {"type": "string", "enum": ["json", "csv", "html"], "default": "json"},
                            "output_path": {"type": "string", "description": "Output file path"}
                        },
                        "required": ["name", "output_path"]
                    }
                ),
                types.Tool(
                    name="filter_data",
                    description="Filter dataset based on conditions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Dataset name"},
                            "conditions": {"type": "array", "items": {"type": "object"}, "description": "Filter conditions"},
                            "new_name": {"type": "string", "description": "Name for filtered dataset"}
                        },
                        "required": ["name", "conditions", "new_name"]
                    }
                )
            ]
            
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle tool execution for data analysis."""
            
            if not PANDAS_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text="Error: pandas is required for data analysis features. Please install pandas."
                )]
            
            try:
                logger.info(f"Executing tool: {name} with arguments: {arguments}")
                
                if name == "load_dataset":
                    path = arguments["path"]
                    dataset_name = arguments["name"]
                    delimiter = arguments.get("delimiter", ",")
                    
                    if not os.path.exists(path):
                        return [types.TextContent(type="text", text=f"File not found: {path}")]
                    
                    # Load dataset based on file extension
                    if path.endswith('.csv'):
                        df = pd.read_csv(path, delimiter=delimiter)
                    elif path.endswith('.json'):
                        df = pd.read_json(path)
                    else:
                        return [types.TextContent(type="text", text="Unsupported file format. Use CSV or JSON.")]
                    
                    self.datasets[dataset_name] = df
                    
                    result = f"Dataset '{dataset_name}' loaded successfully!\n"
                    result += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
                    result += f"Columns: {list(df.columns)}\n"
                    result += f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB"
                    
                    logger.info(f"Successfully loaded dataset '{dataset_name}' with shape {df.shape}")
                    self.analysis_history.append({
                        "action": "load_dataset",
                        "dataset": dataset_name,
                        "timestamp": datetime.now().isoformat(),
                        "details": {"shape": df.shape, "columns": list(df.columns)}
                    })
                    
                    return [types.TextContent(type="text", text=result)]
                
                elif name == "dataset_info":
                    dataset_name = arguments["name"]
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found. Load it first.")]
                    
                    df = self.datasets[dataset_name]
                    
                    info = {
                        "name": dataset_name,
                        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
                        "columns": {
                            "names": list(df.columns),
                            "types": df.dtypes.astype(str).to_dict(),
                            "null_counts": df.isnull().sum().to_dict(),
                            "unique_counts": df.nunique().to_dict()
                        },
                        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
                        "sample_data": df.head().to_dict(orient='records')
                    }
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Dataset Information:\n{json.dumps(info, indent=2, default=str)}"
                    )]
                
                elif name == "calculate_statistics":
                    dataset_name = arguments["name"]
                    columns = arguments.get("columns")
                    include_percentiles = arguments.get("include_percentiles", True)
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name]
                    
                    if columns:
                        df_subset = df[columns]
                    else:
                        df_subset = df.select_dtypes(include=[np.number])
                    
                    if include_percentiles:
                        stats = df_subset.describe(percentiles=[.25, .5, .75, .9, .95])
                    else:
                        stats = df_subset.describe()
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Descriptive Statistics for '{dataset_name}':\n{stats.to_string()}"
                    )]
                
                elif name == "find_correlations":
                    dataset_name = arguments["name"]
                    method = arguments.get("method", "pearson")
                    threshold = arguments.get("threshold", 0.5)
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name]
                    numeric_df = df.select_dtypes(include=[np.number])
                    
                    corr_matrix = numeric_df.corr(method=method)
                    
                    # Find high correlations
                    high_corr = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_val = corr_matrix.iloc[i, j]
                            if abs(corr_val) >= threshold:
                                high_corr.append({
                                    "column1": corr_matrix.columns[i],
                                    "column2": corr_matrix.columns[j],
                                    "correlation": round(corr_val, 3),
                                    "strength": "Strong" if abs(corr_val) >= 0.7 else "Moderate"
                                })
                    
                    result = f"Correlation Analysis ({method}) for '{dataset_name}':\n\n"
                    result += f"High correlations (threshold: {threshold}):\n"
                    
                    for corr in sorted(high_corr, key=lambda x: abs(x["correlation"]), reverse=True):
                        result += f"• {corr['column1']} ↔ {corr['column2']}: {corr['correlation']} ({corr['strength']})\n"
                    
                    if not high_corr:
                        result += "No correlations found above the threshold.\n"
                    
                    result += f"\nFull correlation matrix:\n{corr_matrix.round(3).to_string()}"
                    
                    return [types.TextContent(type="text", text=result)]
                
                elif name == "group_analysis":
                    dataset_name = arguments["name"]
                    group_by = arguments["group_by"]
                    agg_columns = arguments.get("agg_columns")
                    operations = arguments.get("operations", ["mean", "count"])
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name]
                    
                    if group_by not in df.columns:
                        return [types.TextContent(type="text", text=f"Column '{group_by}' not found in dataset.")]
                    
                    if agg_columns:
                        df_agg = df.groupby(group_by)[agg_columns].agg(operations)
                    else:
                        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                        df_agg = df.groupby(group_by)[numeric_cols].agg(operations)
                    
                    result = f"Group Analysis for '{dataset_name}' grouped by '{group_by}':\n\n"
                    result += df_agg.to_string()
                    
                    return [types.TextContent(type="text", text=result)]
                
                elif name == "data_quality_check":
                    dataset_name = arguments["name"]
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name]
                    
                    quality_report = {
                        "dataset": dataset_name,
                        "total_rows": len(df),
                        "total_columns": len(df.columns),
                        "missing_data": {
                            "columns_with_missing": df.columns[df.isnull().any()].tolist(),
                            "missing_percentages": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
                            "total_missing_values": df.isnull().sum().sum()
                        },
                        "duplicates": {
                            "duplicate_rows": df.duplicated().sum(),
                            "duplicate_percentage": round(df.duplicated().sum() / len(df) * 100, 2)
                        },
                        "data_types": df.dtypes.astype(str).to_dict(),
                        "unique_values": df.nunique().to_dict(),
                        "potential_issues": []
                    }
                    
                    # Identify potential issues
                    for col in df.columns:
                        if df[col].isnull().sum() > 0:
                            missing_pct = df[col].isnull().sum() / len(df) * 100
                            if missing_pct > 50:
                                quality_report["potential_issues"].append(f"Column '{col}' has {missing_pct:.1f}% missing values")
                        
                        if df[col].nunique() == 1:
                            quality_report["potential_issues"].append(f"Column '{col}' has only one unique value")
                        
                        if df[col].nunique() == len(df):
                            quality_report["potential_issues"].append(f"Column '{col}' has all unique values (potential identifier)")
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Data Quality Report:\n{json.dumps(quality_report, indent=2, default=str)}"
                    )]
                
                elif name == "generate_insights":
                    dataset_name = arguments["name"]
                    focus = arguments.get("focus", "overview")
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name]
                    insights = []
                    
                    if focus in ["overview", "all"]:
                        insights.append(f"📊 Dataset Overview:")
                        insights.append(f"• Contains {len(df)} records with {len(df.columns)} features")
                        insights.append(f"• Data types: {df.dtypes.value_counts().to_dict()}")
                        
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        if len(numeric_cols) > 0:
                            insights.append(f"• {len(numeric_cols)} numeric columns for analysis")
                    
                    if focus in ["outliers", "all"]:
                        insights.append(f"\n🔍 Outlier Detection:")
                        numeric_df = df.select_dtypes(include=[np.number])
                        for col in numeric_df.columns:
                            Q1 = numeric_df[col].quantile(0.25)
                            Q3 = numeric_df[col].quantile(0.75)
                            IQR = Q3 - Q1
                            outliers = len(numeric_df[(numeric_df[col] < Q1 - 1.5*IQR) | 
                                                    (numeric_df[col] > Q3 + 1.5*IQR)])
                            if outliers > 0:
                                insights.append(f"• {col}: {outliers} potential outliers detected")
                    
                    if focus in ["patterns", "all"]:
                        insights.append(f"\n📈 Pattern Analysis:")
                        # Find columns with high cardinality
                        for col in df.columns:
                            unique_ratio = df[col].nunique() / len(df)
                            if unique_ratio > 0.95:
                                insights.append(f"• {col}: High uniqueness ({unique_ratio:.2%}) - potential identifier")
                            elif unique_ratio < 0.05:
                                insights.append(f"• {col}: Low uniqueness ({unique_ratio:.2%}) - limited variability")
                    
                    if focus in ["recommendations", "all"]:
                        insights.append(f"\n💡 Recommendations:")
                        
                        # Missing data recommendations
                        missing_cols = df.columns[df.isnull().any()].tolist()
                        if missing_cols:
                            insights.append(f"• Address missing data in: {', '.join(missing_cols)}")
                        
                        # Correlation recommendations
                        numeric_df = df.select_dtypes(include=[np.number])
                        if len(numeric_df.columns) > 1:
                            insights.append("• Perform correlation analysis to identify relationships")
                            insights.append("• Consider feature selection for highly correlated variables")
                        
                        # Data type recommendations
                        for col in df.columns:
                            if df[col].dtype == 'object':
                                try:
                                    pd.to_numeric(df[col])
                                    insights.append(f"• Consider converting '{col}' to numeric type")
                                except:
                                    pass
                    
                    self.analysis_history.append({
                        "action": "generate_insights",
                        "dataset": dataset_name,
                        "focus": focus,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return [types.TextContent(
                        type="text",
                        text=f"Data Insights for '{dataset_name}':\n\n" + "\n".join(insights)
                    )]
                
                elif name == "export_analysis":
                    dataset_name = arguments["name"]
                    format_type = arguments.get("format", "json")
                    output_path = arguments["output_path"]
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name]
                    
                    # Create output directory if it doesn't exist
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    
                    if format_type == "csv":
                        df.to_csv(output_path, index=False)
                    elif format_type == "json":
                        analysis_report = {
                            "dataset_name": dataset_name,
                            "shape": df.shape,
                            "columns": list(df.columns),
                            "dtypes": df.dtypes.astype(str).to_dict(),
                            "statistics": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
                            "missing_data": df.isnull().sum().to_dict(),
                            "sample_data": df.head().to_dict(orient='records'),
                            "export_timestamp": datetime.now().isoformat()
                        }
                        with open(output_path, 'w') as f:
                            json.dump(analysis_report, f, indent=2, default=str)
                    elif format_type == "html":
                        html_content = f"""
                        <!DOCTYPE html>
                        <html>
                        <head><title>Data Analysis Report - {dataset_name}</title></head>
                        <body>
                        <h1>Data Analysis Report: {dataset_name}</h1>
                        <h2>Dataset Overview</h2>
                        <p>Shape: {df.shape[0]} rows, {df.shape[1]} columns</p>
                        <h2>Sample Data</h2>
                        {df.head(10).to_html()}
                        <h2>Statistics</h2>
                        {df.describe().to_html() if len(df.select_dtypes(include=[np.number]).columns) > 0 else '<p>No numeric columns for statistics</p>'}
                        </body>
                        </html>
                        """
                        with open(output_path, 'w') as f:
                            f.write(html_content)
                    
                    logger.info(f"Exported analysis for '{dataset_name}' to {output_path}")
                    return [types.TextContent(
                        type="text",
                        text=f"Successfully exported '{dataset_name}' analysis to {output_path} ({format_type} format)"
                    )]
                
                elif name == "filter_data":
                    dataset_name = arguments["name"]
                    conditions = arguments["conditions"]
                    new_name = arguments["new_name"]
                    
                    if dataset_name not in self.datasets:
                        return [types.TextContent(type="text", text=f"Dataset '{dataset_name}' not found.")]
                    
                    df = self.datasets[dataset_name].copy()
                    original_shape = df.shape
                    
                    # Apply filters (simplified implementation)
                    for condition in conditions:
                        if "column" in condition and "operator" in condition and "value" in condition:
                            col = condition["column"]
                            op = condition["operator"]
                            val = condition["value"]
                            
                            if col in df.columns:
                                if op == "==":
                                    df = df[df[col] == val]
                                elif op == "!=":
                                    df = df[df[col] != val]
                                elif op == ">":
                                    df = df[df[col] > val]
                                elif op == "<":
                                    df = df[df[col] < val]
                                elif op == ">=":
                                    df = df[df[col] >= val]
                                elif op == "<=":
                                    df = df[df[col] <= val]
                    
                    self.datasets[new_name] = df
                    
                    result = f"Filtered dataset '{dataset_name}' → '{new_name}'\n"
                    result += f"Original shape: {original_shape}\n"
                    result += f"Filtered shape: {df.shape}\n"
                    result += f"Filters applied: {len(conditions)}"
                    
                    logger.info(f"Created filtered dataset '{new_name}' from '{dataset_name}'")
                    return [types.TextContent(type="text", text=result)]
                
                else:
                    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
                    
            except Exception as e:
                logger.error(f"Error executing tool '{name}': {str(e)}", exc_info=True)
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[types.Resource]:
            """List available resources."""
            resources = [
                types.Resource(
                    uri=AnyUrl("data://loaded_datasets"),
                    name="Loaded Datasets",
                    description="Information about currently loaded datasets",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri=AnyUrl("data://analysis_guide"),
                    name="Data Analysis Guide",
                    description="Guide for performing data analysis with this server",
                    mimeType="text/plain"
                ),
                types.Resource(
                    uri=AnyUrl("data://analysis_history"),
                    name="Analysis History",
                    description="History of analysis operations performed",
                    mimeType="application/json"
                )
            ]
            
            # Add resources for each loaded dataset
            for dataset_name in self.datasets.keys():
                resources.append(
                    types.Resource(
                        uri=AnyUrl(f"data://dataset/{dataset_name}"),
                        name=f"Dataset: {dataset_name}",
                        description=f"Detailed information about {dataset_name} dataset",
                        mimeType="application/json"
                    )
                )
            
            return resources
        
        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            """Handle resource reading."""
            uri_str = str(uri)
            
            if uri_str == "data://loaded_datasets":
                dataset_info = {}
                for name, df in self.datasets.items():
                    dataset_info[name] = {
                        "shape": df.shape,
                        "columns": list(df.columns),
                        "dtypes": df.dtypes.astype(str).to_dict(),
                        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024)
                    }
                return json.dumps(dataset_info, indent=2, default=str)
            
            elif uri_str == "data://analysis_guide":
                guide = """
# Data Analysis MCP Server Guide

This server provides comprehensive data analysis capabilities for data analysts.

## Workflow:

1. **Load Dataset**: Use `load_dataset` to load CSV or JSON files
2. **Explore Data**: Use `dataset_info` to understand your data structure
3. **Quality Check**: Run `data_quality_check` to identify issues
4. **Statistical Analysis**: Use `calculate_statistics` for descriptive stats
5. **Find Relationships**: Use `find_correlations` to discover patterns
6. **Group Analysis**: Use `group_analysis` for segmentation
7. **Get Insights**: Use `generate_insights` for automated recommendations

## Example Workflow:

```
1. load_dataset(path="data/sales.csv", name="sales")
2. dataset_info(name="sales")
3. data_quality_check(name="sales")
4. calculate_statistics(name="sales")
5. find_correlations(name="sales", threshold=0.5)
6. group_analysis(name="sales", group_by="region")
7. generate_insights(name="sales", focus="recommendations")
```

## Tips for Data Analysts:

- Always start with data quality checks
- Use correlation analysis to identify multicollinearity
- Group analysis is perfect for segmentation studies
- Automated insights help identify patterns you might miss
- Clean your data before statistical analysis

## Supported Formats:
- CSV files (with custom delimiters)
- JSON files
- Pandas-compatible formats

## Statistical Methods:
- Descriptive statistics (mean, median, std, etc.)
- Correlation analysis (Pearson, Spearman, Kendall)
- Outlier detection (IQR method)
- Missing data analysis
- Unique value analysis
"""
                return guide.strip()
            
            elif uri_str == "data://analysis_history":
                return json.dumps(self.analysis_history, indent=2, default=str)
            
            elif uri_str.startswith("data://dataset/"):
                dataset_name = uri_str.split("/")[-1]
                if dataset_name in self.datasets:
                    df = self.datasets[dataset_name]
                    info = {
                        "name": dataset_name,
                        "shape": df.shape,
                        "columns": list(df.columns),
                        "dtypes": df.dtypes.astype(str).to_dict(),
                        "sample_data": df.head(10).to_dict(orient='records'),
                        "summary_statistics": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
                        "missing_data": df.isnull().sum().to_dict(),
                        "unique_counts": df.nunique().to_dict()
                    }
                    return json.dumps(info, indent=2, default=str)
                else:
                    raise ValueError(f"Dataset '{dataset_name}' not found")
            
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
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
    """Main entry point for the data analysis server."""
    logger.info("Starting Data Analysis MCP Server...")
    
    if not PANDAS_AVAILABLE:
        logger.error("pandas is required for data analysis features")
        print("Error: pandas is required for data analysis features.", file=sys.stderr)
        print("Install with: pip install pandas numpy", file=sys.stderr)
        sys.exit(1)
    
    logger.info("Data analysis tools ready for use!")
    print("Data analysis tools ready for use!", file=sys.stderr)
    
    try:
        server = DataAnalysisMCPServer()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


# Export the class for importing
__all__ = ["DataAnalysisMCPServer"]


if __name__ == "__main__":
    main()