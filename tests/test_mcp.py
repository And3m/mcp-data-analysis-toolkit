#!/usr/bin/env python3
"""
Test script for MCP Python examples.
Verifies that all servers and clients work correctly.
"""

import asyncio
import csv
import json
import os
import sys
import subprocess
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import mcp
        print("+ MCP module imported successfully")
    except ImportError as e:
        print(f"- MCP import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("+ Pandas available for data analysis")
    except ImportError:
        print("! Pandas not available - data analysis features will be limited")
    
    return True

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "src/mcp_servers/basic_server.py",
        "src/mcp_servers/advanced_server.py", 
        "src/mcp_servers/data_analysis_server.py",
        "src/clients/client_example.py",
        "data/sample_data.csv",
        "config/server_config.json",
        "docs/setup/getting-started.md",
        "docs/api/api-reference.md",
        "docs/api/examples.md",
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"+ {file_path}")
        else:
            print(f"- {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_server_startup(server_script, timeout=5):
    """Test that a server can start without errors."""
    print(f"\nTesting {server_script} startup...")
    
    try:
        # Start server process
        process = subprocess.Popen(
            [sys.executable, server_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait briefly to see if it starts without immediate errors
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"+ {server_script} started successfully")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"- {server_script} failed to start")
            if stderr:
                print(f"  Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"- Error testing {server_script}: {e}")
        return False

def test_sample_data():
    """Test that sample data is valid."""
    print("\nTesting sample data...")
    
    try:
        import pandas as pd
        df = pd.read_csv("data/sample_data.csv")
        
        expected_columns = ["name", "age", "department", "salary", "experience_years", "performance_score"]
        
        if list(df.columns) == expected_columns:
            print(f"+ Sample data has correct columns")
        else:
            print(f"- Sample data columns mismatch. Expected: {expected_columns}, Got: {list(df.columns)}")
            return False
        
        if len(df) > 0:
            print(f"+ Sample data has {len(df)} rows")
        else:
            print("- Sample data is empty")
            return False
        
        return True
        
    except ImportError:
        print("! Pandas not available - skipping sample data validation")
        return True
    except Exception as e:
        print(f"- Error reading sample data: {e}")
        return False

async def test_basic_client():
    """Test basic client functionality."""
    print("\nTesting basic client functionality...")
    
    try:
        from src.clients.client_example import MCPClientExample
        
        client = MCPClientExample()
        
        # Test server startup (basic server)
        server_cmd = [sys.executable, "src/mcp_servers/basic_server.py"]
        
        if await client.connect_to_server(server_cmd):
            print("+ Client connected to basic server")
            
            # Test listing tools
            tools = await client.list_tools()
            if len(tools) > 0:
                print(f"+ Listed {len(tools)} tools")
            else:
                print("- No tools found")
                return False
            
            # Test calling a simple tool
            result = await client.call_tool("calculator", {"expression": "2 + 2"})
            if result and "4" in str(result):
                print("+ Calculator tool working")
            else:
                print("- Calculator tool failed")
                return False
            
            await client.disconnect()
            print("+ Client disconnected successfully")
            return True
        else:
            print("- Failed to connect to basic server")
            return False
            
    except Exception as e:
        print(f"- Error testing client: {e}")
        return False

def main():
    """Run all tests."""
    print("MCP Python Examples Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Sample Data Test", test_sample_data),
        ("Basic Server Startup", lambda: test_server_startup("src/mcp_servers/basic_server.py")),
        ("Advanced Server Startup", lambda: test_server_startup("src/mcp_servers/advanced_server.py")),
        ("Data Analysis Server Startup", lambda: test_server_startup("src/mcp_servers/data_analysis_server.py"))
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"- {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Test client functionality
    try:
        client_result = asyncio.run(test_basic_client())
        results.append(("Client Functionality", client_result))
    except Exception as e:
        print(f"- Client test failed with exception: {e}")
        results.append(("Client Functionality", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("** All tests passed! Your MCP setup is working correctly.")
        print("\nNext steps:")
        print("1. Run: python src/clients/client_example.py")
        print("2. Try: python src/clients/client_example.py interactive")
        print("3. Try: python src/clients/client_example.py data")
        print("4. Run enhanced tests: python tests/test_enhanced_mcp.py")
        print("5. Explore the documentation in docs/")
    else:
        print("** Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that you're in the correct directory")
        print("3. Verify Python version is 3.8 or higher")
        print("4. Check log files for detailed error information")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)