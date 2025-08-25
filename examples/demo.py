#!/usr/bin/env python3
"""
Simple MCP Demo Script

This script demonstrates MCP server functionality by running
the servers and showing their capabilities without complex client patterns.
"""

import subprocess
import sys
import time
import os

def run_server_demo(server_name, server_script):
    """Run a brief demo of a server."""
    print(f"\n{'='*60}")
    print(f"DEMONSTRATING {server_name}")
    print(f"{'='*60}")
    
    print(f"Starting {server_name}...")
    
    try:
        # Start server process
        process = subprocess.Popen(
            [sys.executable, server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait briefly to see server output
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✓ {server_name} started successfully!")
            print(f"  Server is running and ready to accept connections")
            print(f"  To connect: python {server_script}")
            
            # Show server stderr output (which contains startup messages)
            process.terminate()
            stdout, stderr = process.communicate()
            
            if stderr:
                print(f"\nServer startup messages:")
                for line in stderr.split('\n')[:5]:  # Show first 5 lines
                    if line.strip():
                        print(f"  {line}")
            
        else:
            stdout, stderr = process.communicate()
            print(f"✗ {server_name} failed to start")
            if stderr:
                print(f"Error: {stderr}")
        
    except Exception as e:
        print(f"Error testing {server_name}: {e}")

def show_capabilities():
    """Show the capabilities of each server."""
    print(f"\n{'='*60}")
    print("MCP SERVER CAPABILITIES")
    print(f"{'='*60}")
    
    capabilities = {
        "Basic Server": {
            "tools": ["calculator", "string_utils", "get_current_time"],
            "resources": ["system_info", "server_config", "help"],
            "use_cases": ["Learning MCP", "Simple automation", "Basic calculations"]
        },
        "Advanced Server": {
            "tools": ["file_read", "file_write", "directory_list", "csv_analyze"],
            "resources": ["capabilities", "temp_workspace"],
            "use_cases": ["File management", "Data processing", "Advanced automation"]
        },
        "Data Analysis Server": {
            "tools": ["load_dataset", "dataset_info", "calculate_statistics", "find_correlations", "group_analysis", "data_quality_check", "generate_insights"],
            "resources": ["loaded_datasets", "analysis_guide", "dataset metadata"],
            "use_cases": ["Business intelligence", "Statistical analysis", "Data science"]
        }
    }
    
    for server_name, caps in capabilities.items():
        print(f"\n{server_name}:")
        print(f"  Tools: {', '.join(caps['tools'])}")
        print(f"  Resources: {', '.join(caps['resources'])}")
        print(f"  Best for: {', '.join(caps['use_cases'])}")

def show_sample_data():
    """Show sample data information."""
    print(f"\n{'='*60}")
    print("SAMPLE DATA")
    print(f"{'='*60}")
    
    if os.path.exists("data/sample_data.csv"):
        print("Employee dataset (data/sample_data.csv):")
        
        try:
            with open("data/sample_data.csv", 'r') as f:
                lines = f.readlines()
                print(f"  Columns: {lines[0].strip()}")
                print(f"  Rows: {len(lines) - 1}")
                print(f"  Sample data:")
                for i, line in enumerate(lines[1:4]):  # Show first 3 data rows
                    print(f"    {line.strip()}")
                if len(lines) > 4:
                    print("    ...")
                    
        except Exception as e:
            print(f"  Error reading sample data: {e}")
    else:
        print("Sample data file not found")

def show_usage_examples():
    """Show example usage commands."""
    print(f"\n{'='*60}")
    print("USAGE EXAMPLES")
    print(f"{'='*60}")
    
    examples = [
        ("Start Basic Server", "python src/mcp_servers/basic_server.py"),
        ("Start Data Analysis Server", "python src/mcp_servers/data_analysis_server.py"),
        ("Run Client Demo (Basic)", "python src/clients/client_example.py basic"),
        ("Run Client Demo (Data)", "python src/clients/client_example.py data"),
        ("Interactive Client", "python src/clients/client_example.py interactive"),
        ("Run All Tests", "python tests/test_mcp.py")
    ]
    
    print("Try these commands:")
    for description, command in examples:
        print(f"  {description:25} : {command}")

def main():
    """Main demo function."""
    print("MCP Python Examples Demo")
    print("This demonstrates the Model Context Protocol (MCP) servers")
    
    # Show what MCP is
    print(f"\n{'='*60}")
    print("WHAT IS MCP?")
    print(f"{'='*60}")
    print("Model Context Protocol (MCP) is an open standard that enables")
    print("AI applications to securely connect with external data sources and tools.")
    print("It acts as a universal bridge between AI models and your data/systems.")
    
    # Show capabilities
    show_capabilities()
    
    # Show sample data
    show_sample_data()
    
    # Demo each server
    servers = [
        ("Basic MCP Server", "src/mcp_servers/basic_server.py"),
        ("Advanced MCP Server", "src/mcp_servers/advanced_server.py"),
        ("Data Analysis MCP Server", "src/mcp_servers/data_analysis_server.py")
    ]
    
    for server_name, server_script in servers:
        run_server_demo(server_name, server_script)
    
    # Show usage examples
    show_usage_examples()
    
    print(f"\n{'='*60}")
    print("DEMO COMPLETE")
    print(f"{'='*60}")
    print("🎉 All MCP servers are working correctly!")
    print("\nNext steps:")
    print("1. Read the documentation: docs/getting_started.md")
    print("2. Try the interactive client: python examples/client_example.py interactive")
    print("3. Explore the API reference: docs/api_reference.md")
    print("4. Build your own MCP server using the examples as templates")
    
if __name__ == "__main__":
    main()