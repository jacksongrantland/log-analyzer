# Structured Log Analyzer Project

## Goal
Build a simple software-engineering-oriented project in one day that analyzes structured and semi-structured log files to surface useful debugging information.

## Main Use Case
Applications, servers, scripts, and services often generate logs that contain:
- `ERROR`
- `WARNING` or `WARN`
- `INFO`
- optional timestamps
- optional module or source names
- human-readable messages

This project should help a user:
1. Count how many errors, warnings, and info messages appear
2. Find repeated messages or repeated error patterns
3. Identify the most common issues in a log file
4. Quickly summarize system behavior without manually reading the entire file

## Design Direction
The analyzer should **adapt to common log styles** instead of forcing users to rewrite their logs to match one strict format.

That means:
- do **not** require a custom log file format
- do support common patterns using keyword detection and lightweight parsing
- work with both structured and semi-structured logs

## Supported Log Examples

### Example 1: Simple structured logs
```text
2026-04-01 10:32:15 ERROR Failed to connect to database
2026-04-01 10:32:20 INFO Server started
2026-04-01 10:32:30 WARNING High memory usage
```

### Example 2: Semi-structured logs
```text
[2026-04-01 10:32:15] ERROR AuthService: Invalid token
[2026-04-01 10:32:18] INFO User logged in
[2026-04-01 10:32:25] WARN Cache nearing limit
```

### Example 3: Mixed log style
```text
ERROR: Database connection failed
INFO Server started successfully
WARN CPU temperature high
```

## Core Requirements
Build a command-line tool that:
- accepts a log file path as input
- reads the file line by line
- identifies log levels such as `ERROR`, `WARNING`, `WARN`, and `INFO`
- counts occurrences by level
- finds repeated messages
- prints a summary report

## Minimum Viable Features
- Parse a file passed like:
```bash
python analyzer.py sample.log
```

- Output:
  - total lines processed
  - number of errors
  - number of warnings
  - number of info messages
  - top repeated error or warning messages

## Nice-to-Have Features
If time allows, add one or more of these:
- support CSV or JSON output
- filter results by level
- show timestamps if found
- group messages by source/module if present
- ignore duplicate whitespace or formatting noise
- support large files efficiently
- add unit tests

## Suggested File Structure
```text
log-analyzer/
├── analyzer.py
├── sample.log
├── README.md
└── tests/
    └── test_analyzer.py
```

## Parsing Strategy
Do not try to perfectly support every real-world format.

Use a practical approach:
1. Read each line
2. Search for keywords like:
   - `ERROR`
   - `WARNING`
   - `WARN`
   - `INFO`
3. Extract the rest of the line as the message
4. Normalize repeated messages if possible
5. Aggregate counts

## Suggested Logic
- If a line contains `ERROR`, count it as an error
- If a line contains `WARNING` or `WARN`, count it as a warning
- If a line contains `INFO`, count it as info
- Store the message portion in a frequency map
- At the end, sort repeated messages by count

## Example Output
```text
Log Summary
-----------
Total lines processed: 120
Errors: 14
Warnings: 9
Info: 97

Top Repeated Issues
-------------------
Database connection failed - 6
Invalid token - 4
Cache nearing limit - 3
```

## Resume Framing
This project should be described as a software engineering tool, not just a script.

Possible resume bullets:
- Built a log analysis tool to parse structured and semi-structured application logs and identify recurring error patterns
- Implemented file parsing and aggregation logic to summarize system health and common failures
- Designed a command-line utility for debugging workflows and fast issue triage

## AI Build Prompt
Use a prompt like this with an AI coding assistant:

```text
Build me a Python command-line log analyzer project.

Requirements:
- Accept a log file path as a command-line argument
- Read the file line by line
- Detect log levels such as ERROR, WARNING/WARN, and INFO
- Count occurrences of each level
- Extract and count repeated messages
- Print a clear summary report
- Handle structured and semi-structured log formats
- Organize the code cleanly with functions
- Include comments and readable variable names
- Add a small sample log file
- Keep the project simple but professional
```

## What to Say If Asked About It
If someone asks what the project does, say:

> It analyzes application or server logs to help identify recurring errors, warning patterns, and general system behavior. I built it as a lightweight debugging and monitoring tool that can work with common structured and semi-structured logs.

## Next Improvement Ideas
After the first version works, possible upgrades include:
- regex-based parsing for timestamps and modules
- JSON export
- HTML summary report
- web UI using Flask or FastAPI
- dashboard charts
- anomaly detection for unusual spikes in errors
