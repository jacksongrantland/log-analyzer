# Structured Log Analyzer

A command-line tool to analyze structured and semi-structured log files, providing summaries of errors, warnings, and info messages, along with identifying repeated issues for efficient debugging and monitoring.

## Features

- Parses common log formats (structured and semi-structured)
- Counts occurrences of ERROR, WARNING/WARN, INFO, DEBUG, CRITICAL, TRACE, and FATAL messages
- Extracts and displays timestamp range (earliest and latest) if present
- Extracts and groups messages by source/module (e.g., AuthService) if present
- Case-insensitive message normalization for better deduplication
- Identifies and ranks repeated error/warning messages
- Command-line interface for easy integration into workflows
- Handles large files efficiently by processing line by line

## Usage

```bash
python analyzer.py <log_file>
```

### Example

```bash
python analyzer.py sample.log
```

Output:
```
Log Summary
-----------
Total lines processed: 20
Errors: 7
Warnings: 6
Info: 7
Debugs: 0
Criticals: 0
Traces: 0
Fatals: 0

No timestamps found in log.

Top Repeated Issues
-------------------
FAILED TO CONNECT TO DATABASE - 4
HIGH MEMORY USAGE - 4
INVALID AUTHENTICATION TOKEN - 3
CACHE NEARING LIMIT - 2
SERVER STARTED - 1
```

For logs with timestamps and additional levels:

```bash
python analyzer.py sample_extended.log
```

Output:
```
Log Summary
-----------
Total lines processed: 30
Errors: 8
Warnings: 6
Info: 7
Debugs: 3
Criticals: 3
Traces: 2
Fatals: 1

Earliest timestamp: 2026-04-01T10:32:15
Latest timestamp: 2026-04-01T10:34:45

Top Repeated Issues
-------------------
FAILED TO CONNECT TO DATABASE - 4
HIGH MEMORY USAGE - 4
INVALID AUTHENTICATION TOKEN - 3
CACHE NEARING LIMIT - 2
SERVER STARTED - 1
```

## Requirements

- Python 3.6+

## Installation

1. Clone or download the project files
2. Ensure Python 3 is installed
3. Run the analyzer with a log file path

## Supported Log Formats

The analyzer adapts to common log styles without requiring strict formatting:

- `2026-04-01 10:32:15 ERROR Failed to connect to database`
- `[2026-04-01 10:32:15] ERROR AuthService: Invalid token`
- `ERROR: Database connection failed`

## Project Structure

```
log-analyzer/
├── analyzer.py          # Main analysis script
├── sample.log           # Example log file
├── README.md            # This file
└── tests/
    └── test_analyzer.py # Unit tests
```

## Development

This project demonstrates software engineering practices including:
- Modular code design with functions
- Error handling and input validation
- Clean, readable code with comments
- Command-line interface design
- Basic testing structure

## Future Enhancements

- Support for CSV/JSON output formats
- Filtering by log level or time range
- Timestamp extraction and analysis
- Module/source grouping
- Web-based dashboard
- Anomaly detection for error spikes