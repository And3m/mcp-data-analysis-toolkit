# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-08-25

### Added
- **Multi-format Export**: Export analysis results to JSON, CSV, and HTML formats
- **Dynamic Data Filtering**: Filter datasets with complex conditions and create new filtered datasets
- **Analysis History Tracking**: Track all analysis operations with timestamps and details
- **Enhanced Logging**: Structured logging with file and console output for monitoring and debugging
- **Security Enhancements**: Safe expression evaluation with comprehensive input validation
- **Performance Monitoring**: Track dataset operations and memory usage
- **Enhanced Test Suite**: Comprehensive test coverage with 13+ test cases covering all functionality
- **Error Scenario Testing**: Tests for edge cases and error conditions
- **New MCP Tools**:
  - `export_analysis`: Export analysis results in multiple formats
  - `filter_data`: Create filtered datasets based on conditions
  - `analysis_history`: View history of all analysis operations
- **New Dependencies**: Added support for visualization libraries (matplotlib, seaborn), enhanced logging (structlog, rich), and additional utilities

### Enhanced
- **Data Analysis Server**: Improved with better error handling, logging, and additional capabilities
- **Error Handling**: Comprehensive error handling across all modules with detailed logging
- **Input Validation**: Enhanced validation for all tool inputs and parameters
- **Documentation**: Updated README with new features and capabilities
- **Test Coverage**: Expanded test suite covering all new functionality
- **Dependencies**: Updated requirements.txt and pyproject.toml with additional packages

### Security
- **Safe Expression Evaluation**: Implemented secure mathematical expression parsing
- **Input Sanitization**: Added comprehensive input validation and sanitization
- **Access Controls**: Enhanced file access controls and path validation

### Performance
- **Memory Tracking**: Added memory usage monitoring for datasets
- **Async Operations**: Maintained async patterns for scalable performance
- **Resource Management**: Improved resource cleanup and management

## [1.0.0] - 2025-08-25

### Added
- Initial release of MCP Data Analysis Toolkit
- **Basic MCP Server**: Fundamental tools (calculator, string utilities, time functions)
- **Advanced MCP Server**: File operations and enhanced processing
- **Data Analysis Server**: Comprehensive business intelligence toolkit
- **MCP Client**: Example client for interacting with all servers
- **Claude Desktop Integration**: Seamless integration with Claude Desktop
- **Core Features**:
  - Dataset loading (CSV, JSON)
  - Statistical analysis and summaries
  - Correlation discovery
  - Data quality assessment
  - Automated insights generation
  - Group analysis and segmentation
- **Documentation**: Comprehensive setup guides and API documentation
- **Testing**: Basic test suite for validation
- **Sample Data**: Included sample datasets for testing

### Infrastructure
- **Python 3.8+ Support**: Compatible with Python 3.8 and higher
- **MCP Protocol**: Full implementation of Model Context Protocol
- **Async Architecture**: Modern async/await patterns
- **Modular Design**: Clean, extensible architecture