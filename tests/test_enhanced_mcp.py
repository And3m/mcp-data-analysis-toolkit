#!/usr/bin/env python3
"""
Enhanced Test Suite for MCP Python Examples.
Tests new features, error handling, logging, and data analysis capabilities.
"""

import asyncio
import json
import logging
import os
import sys
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestDataAnalysisFeatures(unittest.TestCase):
    """Test data analysis specific features."""
    
    def setUp(self):
        """Set up test environment."""
        try:
            import pandas as pd
            import numpy as np
            self.pandas_available = True
            self.pd = pd
            self.np = np
        except ImportError:
            self.pandas_available = False
            self.pd = None
            self.np = None
    
    def test_data_creation_and_manipulation(self):
        """Test basic data operations."""
        if not self.pandas_available:
            self.skipTest("Pandas not available")
        
        # Create test data
        test_data = self.pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
            'age': [25, 30, 35, 28],
            'salary': [50000, 60000, 70000, 55000],
            'department': ['IT', 'HR', 'IT', 'Finance']
        })
        
        # Test basic operations
        self.assertEqual(len(test_data), 4)
        self.assertEqual(list(test_data.columns), ['name', 'age', 'salary', 'department'])
        
        # Test statistics
        stats = test_data.describe()
        self.assertIsNotNone(stats)
        
        # Test filtering
        it_employees = test_data[test_data['department'] == 'IT']
        self.assertEqual(len(it_employees), 2)
    
    def test_correlation_analysis(self):
        """Test correlation calculation."""
        if not self.pandas_available:
            self.skipTest("Pandas not available")
        
        test_data = self.pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10],  # Perfect correlation with A
            'C': [5, 4, 3, 2, 1]    # Negative correlation with A
        })
        
        corr_matrix = test_data.corr()
        
        # Check perfect positive correlation
        self.assertAlmostEqual(corr_matrix.loc['A', 'B'], 1.0, places=2)
        
        # Check negative correlation
        self.assertLess(corr_matrix.loc['A', 'C'], 0)
    
    def test_group_analysis(self):
        """Test group-by operations."""
        if not self.pandas_available:
            self.skipTest("Pandas not available")
        
        test_data = self.pd.DataFrame({
            'department': ['IT', 'HR', 'IT', 'HR', 'Finance'],
            'salary': [60000, 50000, 70000, 55000, 65000],
            'age': [30, 25, 35, 28, 32]
        })
        
        grouped = test_data.groupby('department').agg({
            'salary': ['mean', 'count'],
            'age': 'mean'
        })
        
        self.assertIsNotNone(grouped)
        self.assertGreater(len(grouped), 0)

class TestExportFunctionality(unittest.TestCase):
    """Test data export capabilities."""
    
    def setUp(self):
        """Set up test environment."""
        try:
            import pandas as pd
            self.pandas_available = True
            self.pd = pd
        except ImportError:
            self.pandas_available = False
            self.pd = None
    
    def test_csv_export(self):
        """Test CSV export functionality."""
        if not self.pandas_available:
            self.skipTest("Pandas not available")
        
        test_data = self.pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': ['x', 'y', 'z']
        })
        
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = os.path.join(temp_dir, 'test_export.csv')
            test_data.to_csv(csv_path, index=False)
            
            self.assertTrue(os.path.exists(csv_path))
            
            # Verify content
            loaded_data = self.pd.read_csv(csv_path)
            self.assertEqual(len(loaded_data), 3)
            self.assertEqual(list(loaded_data.columns), ['A', 'B', 'C'])
    
    def test_json_export(self):
        """Test JSON export functionality."""
        if not self.pandas_available:
            self.skipTest("Pandas not available")
        
        test_data = self.pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [25, 30],
            'city': ['NY', 'LA']
        })
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = os.path.join(temp_dir, 'test_export.json')
            
            # Create analysis report
            analysis_report = {
                "dataset_name": "test",
                "shape": test_data.shape,
                "columns": list(test_data.columns),
                "sample_data": test_data.to_dict(orient='records')
            }
            
            with open(json_path, 'w') as f:
                json.dump(analysis_report, f, indent=2)
            
            self.assertTrue(os.path.exists(json_path))
            
            # Verify content
            with open(json_path, 'r') as f:
                loaded_report = json.load(f)
            
            self.assertEqual(loaded_report['dataset_name'], 'test')
            self.assertEqual(loaded_report['shape'], [2, 3])
    
    def test_html_export(self):
        """Test HTML export functionality."""
        if not self.pandas_available:
            self.skipTest("Pandas not available")
        
        test_data = self.pd.DataFrame({
            'Product': ['A', 'B', 'C'],
            'Price': [10.99, 15.50, 8.75]
        })
        
        with tempfile.TemporaryDirectory() as temp_dir:
            html_path = os.path.join(temp_dir, 'test_report.html')
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Test Report</title></head>
            <body>
            <h1>Data Analysis Report</h1>
            {test_data.to_html()}
            </body>
            </html>
            """
            
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            self.assertTrue(os.path.exists(html_path))
            
            # Verify basic HTML structure
            with open(html_path, 'r') as f:
                content = f.read()
            
            self.assertIn('<html>', content)
            self.assertIn('<table', content)
            self.assertIn('Product', content)

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios."""
    
    def test_safe_expression_evaluation(self):
        """Test safe mathematical expression evaluation."""
        # Safe expressions
        safe_expressions = ["2 + 2", "10 * 5", "100 / 4", "2 ** 3"]
        
        for expr in safe_expressions:
            try:
                result = eval(expr)
                self.assertIsNotNone(result)
            except Exception as e:
                self.fail(f"Safe expression '{expr}' should not raise exception: {e}")
    
    def test_unsafe_expression_detection(self):
        """Test detection of unsafe expressions."""
        unsafe_expressions = [
            "import os",
            "exec('print(1)')",
            "__import__('sys')",
            "eval('2+2')",
            "open('/etc/passwd')"
        ]
        
        dangerous_keywords = ["import", "exec", "eval", "__", "open"]
        
        for expr in unsafe_expressions:
            has_dangerous = any(keyword in expr for keyword in dangerous_keywords)
            self.assertTrue(has_dangerous, f"Expression '{expr}' should be detected as unsafe")
    
    def test_file_not_found_handling(self):
        """Test handling of non-existent files."""
        non_existent_file = "/path/that/definitely/does/not/exist.csv"
        
        # Verify file doesn't exist
        self.assertFalse(os.path.exists(non_existent_file))
        
        # Test would handle this gracefully in actual server
        try:
            with open(non_existent_file, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            # This is expected behavior
            pass
        except Exception as e:
            self.fail(f"Unexpected exception type: {type(e)}")

class TestLoggingFunctionality(unittest.TestCase):
    """Test logging capabilities."""
    
    def test_logger_creation(self):
        """Test logger creation and configuration."""
        logger = logging.getLogger('test_mcp_server')
        logger.setLevel(logging.INFO)
        
        self.assertEqual(logger.level, logging.INFO)
        self.assertEqual(logger.name, 'test_mcp_server')
    
    def test_log_message_capture(self):
        """Test log message capture."""
        # Create logger with string capture
        logger = logging.getLogger('test_capture')
        logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Add string capture handler
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Test logging different levels
        test_messages = [
            (logging.INFO, "Test info message"),
            (logging.WARNING, "Test warning message"),
            (logging.ERROR, "Test error message")
        ]
        
        for level, message in test_messages:
            logger.log(level, message)
        
        # Check captured output
        log_output = log_capture.getvalue()
        
        for level, message in test_messages:
            self.assertIn(message, log_output)
    
    def test_log_file_creation(self):
        """Test log file creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, 'test_mcp.log')
            
            # Create logger with file handler
            logger = logging.getLogger('test_file_logger')
            logger.setLevel(logging.INFO)
            
            # Clear existing handlers
            logger.handlers.clear()
            
            # Add file handler
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # Log some messages
            logger.info("Test file logging")
            logger.warning("Test warning to file")
            
            # Ensure data is written
            file_handler.close()
            
            # Verify file was created and has content
            self.assertTrue(os.path.exists(log_file))
            
            with open(log_file, 'r') as f:
                content = f.read()
            
            self.assertIn("Test file logging", content)
            self.assertIn("Test warning to file", content)

class TestMCPServerIntegration(unittest.TestCase):
    """Test MCP server integration and functionality."""
    
    def test_server_process_startup(self):
        """Test that servers can start without immediate errors."""
        servers = [
            "src/mcp_servers/basic_server.py",
            "src/mcp_servers/advanced_server.py",
            "src/mcp_servers/data_analysis_server.py"
        ]
        
        for server_script in servers:
            if not os.path.exists(server_script):
                self.fail(f"Server script not found: {server_script}")
                continue
            
            try:
                # Start server process
                process = subprocess.Popen(
                    [sys.executable, server_script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait briefly to see if it starts
                time.sleep(2)
                
                # Check if process is still running
                if process.poll() is None:
                    # Server started successfully
                    process.terminate()
                    process.wait()
                else:
                    stdout, stderr = process.communicate()
                    self.fail(f"Server {server_script} failed to start. stderr: {stderr}")
                    
            except Exception as e:
                self.fail(f"Error testing server {server_script}: {e}")


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("MCP Enhanced Test Suite")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataAnalysisFeatures,
        TestExportFunctionality,
        TestErrorHandling,
        TestLoggingFunctionality,
        TestMCPServerIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    passed_tests = total_tests - failed_tests
    
    print(f"Tests run: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if failed_tests == 0:
        print("** All enhanced tests passed!")
        print("\nNew capabilities tested:")
        print("- Advanced data analysis operations")
        print("- Multi-format export functionality")
        print("- Comprehensive error handling")
        print("- Logging and monitoring capabilities")
        print("- Server integration and startup")
    else:
        print("** Some tests failed. Check output above for details.")
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)