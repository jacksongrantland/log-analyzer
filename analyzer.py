#!/usr/bin/env python3
"""
Structured Log Analyzer

A command-line tool to analyze log files and provide summaries of errors, warnings, and info messages,
along with identifying repeated issues.
"""

import sys
from collections import defaultdict

def analyze_log(file_path):
    """
    Analyze the log file and return summary statistics.

    Args:
        file_path (str): Path to the log file

    Returns:
        dict: Summary containing counts and repeated messages
    """
    levels = {'ERROR': 0, 'WARNING': 0, 'INFO': 0}
    messages = defaultdict(int)
    total_lines = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                total_lines += 1
                line_upper = line.upper().strip()

                if 'ERROR' in line_upper:
                    levels['ERROR'] += 1
                    # Extract message after ERROR
                    parts = line_upper.split('ERROR', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        messages[msg] += 1
                elif 'WARNING' in line_upper or 'WARN' in line_upper:
                    levels['WARNING'] += 1
                    # Extract message after WARNING or WARN
                    if 'WARNING' in line_upper:
                        parts = line_upper.split('WARNING', 1)
                    else:
                        parts = line_upper.split('WARN', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        messages[msg] += 1
                elif 'INFO' in line_upper:
                    levels['INFO'] += 1
                    # Extract message after INFO
                    parts = line_upper.split('INFO', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        messages[msg] += 1

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Get top repeated messages
    top_messages = sorted(messages.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        'total_lines': total_lines,
        'levels': levels,
        'top_messages': top_messages
    }

def print_summary(summary):
    """Print the analysis summary to stdout."""
    print("Log Summary")
    print("-----------")
    print(f"Total lines processed: {summary['total_lines']}")
    print(f"Errors: {summary['levels']['ERROR']}")
    print(f"Warnings: {summary['levels']['WARNING']}")
    print(f"Info: {summary['levels']['INFO']}")
    print()
    print("Top Repeated Issues")
    print("-------------------")
    if summary['top_messages']:
        for msg, count in summary['top_messages']:
            print(f"{msg} - {count}")
    else:
        print("No repeated issues found.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    summary = analyze_log(log_file)
    print_summary(summary)

if __name__ == "__main__":
    main()