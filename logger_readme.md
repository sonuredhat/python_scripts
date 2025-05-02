# Custom Logger - README

## Overview

This is a custom logging utility implemented in Python to log messages with the following features:

- A unique UUID is generated for each log session, ensuring traceability across logs.
- Logs can be written to both the console and a file.
- The logger supports multiple log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
- Log entries contain the timestamp, log level, unique session UUID, function name, filename, and line number for detailed debugging.
- The log level can be customized for each instance of the logger.

## Features

1. **Unique UUID for Each Log Session**: Every time the logger is initialized, a unique UUID is generated and added to the logs for better traceability across different log entries.
2. **Dual Logging Handlers**:
   - **Console Logging**: Logs are displayed on the console.
   - **File Logging**: Logs are written to a log file, named based on the logger's instance and the current date.
3. **Customizable Log Levels**: The logger allows you to specify which log levels are enabled for logging (e.g., `DEBUG`, `INFO`, `WARNING`, etc.).

## Installation

There is no installation required for this logger as it's a Python class. Simply copy the code into your project, and you can start using it.

## Usage

### 1. Initialize the Logger

You can initialize the logger by creating an instance of the `CustomLogger` class. The `enabled_levels` parameter lets you define which log levels are enabled. The default level is `INFO`.

Example:

```python
# Initialize the logger
logger = CustomLogger("fileNameForLog", enabled_levels={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})

# Set the logger to use the custom logger
logging.basicConfig(level=logging.DEBUG, handlers=[logger.logger.handlers[0]], format="%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(funcName)s:%(lineno)d]")

def raiseLog():
    logger.log_info("this is info Log")
    logger.log_warning("this is warning Log")

# Sample Logs

2025-05-02 12:34:56,789 - INFO_123e4567-e89b-12d3-a456-426614174000 - this is info Log - [raiseLog:example.py:15]
2025-05-02 12:34:56,790 - WARNING_123e4567-e89b-12d3-a456-426614174000 - this is warning Log - [raiseLog:example.py:16]

