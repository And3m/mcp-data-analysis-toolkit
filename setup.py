#!/usr/bin/env python3
"""
Setup script for MCP Data Analysis Toolkit
Provides easy commands to run servers, tests, and demos.
"""

import subprocess
import sys
import os
from pathlib import Path

# Ensure we're in the project root
PROJECT_ROOT = Path(__file__).parent
os.chdir(PROJECT_ROOT)

def run_command(cmd, description):
    """Run a command with description."""
    print(f"\n{'='*60}")
    print(f">> {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"+ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"- {description} failed with error code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"- Command not found: {cmd[0]}")
        return False

def main():
    """Main setup function."""
    print("MCP Data Analysis Toolkit Setup")
    print("Created by Vijay Andem - Data Analyst")
    print("LinkedIn: https://www.linkedin.com/in/vijay-andem-b2092223/")
    print("Twitter: https://x.com/vjandem")
    
    if len(sys.argv) < 2:
        print("""
Usage: python setup.py <command>

Available commands:
  install     - Install all dependencies
  test        - Run comprehensive test suite
  demo        - Run interactive demonstration
  basic       - Start basic MCP server
  advanced    - Start advanced MCP server
  data        - Start data analysis server
  client      - Run client examples
  interactive - Run interactive client session
  all         - Run demo and tests
  help        - Show this help message
        """)
        return

    command = sys.argv[1].lower()
    
    if command == "install":
        success = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                            "Installing Dependencies")
        if success:
            print("+ Ready to use! Try: python setup.py demo")
    
    elif command == "test":
        run_command([sys.executable, "tests/test_mcp.py"], "Running Test Suite")
    
    elif command == "demo":
        run_command([sys.executable, "src/clients/client_example.py"], "Running Client Demo")
    
    elif command == "basic":
        run_command([sys.executable, "src/mcp_servers/basic_server.py"], "Starting Basic MCP Server")
    
    elif command == "advanced":
        run_command([sys.executable, "src/mcp_servers/advanced_server.py"], "Starting Advanced MCP Server")
    
    elif command == "data":
        run_command([sys.executable, "src/mcp_servers/data_analysis_server.py"], "Starting Data Analysis Server")
    
    elif command == "client":
        run_command([sys.executable, "src/clients/client_example.py"], "Running Client Examples")
    
    elif command == "interactive":
        run_command([sys.executable, "src/clients/client_example.py", "interactive"], "Starting Interactive Client")
    
    elif command == "all":
        print("Running complete demonstration...")
        run_command([sys.executable, "src/clients/client_example.py"], "Demo")
        run_command([sys.executable, "tests/test_mcp.py"], "Tests")
    
    elif command == "help":
        # Show usage message directly
        print("""
Usage: python setup.py <command>

Available commands:
  install     - Install all dependencies
  test        - Run comprehensive test suite
  demo        - Run client demonstration
  basic       - Start basic MCP server
  advanced    - Start advanced MCP server
  data        - Start data analysis server
  client      - Run client examples
  interactive - Run interactive client session
  all         - Run demo and tests
  help        - Show this help message
        """)
    
    else:
        print(f"- Unknown command: {command}")
        print("Use 'python setup.py help' for available commands.")

if __name__ == "__main__":
    main()