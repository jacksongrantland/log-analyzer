#!/usr/bin/env python3
"""
Structured Log Analyzer

A command-line tool to analyze log files and provide summaries of errors, warnings, and info messages,
along with identifying repeated issues.
"""

import sys
from collections import defaultdict
import datetime
import re

def analyze_log(file_path):
    """
    Analyze the log file and return summary statistics.

    Args:
        file_path (str): Path to the log file

    Returns:
        dict: Summary containing counts and repeated messages
    """
    levels = {'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0, 'CRITICAL': 0, 'TRACE': 0, 'FATAL': 0}
    messages = defaultdict(int)
    timestamps = []
    sources = defaultdict(int)
    total_lines = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                total_lines += 1
                line_upper = line.upper().strip()

                # Extract timestamp if present
                timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                if timestamp_match:
                    try:
                        ts = datetime.datetime.strptime(timestamp_match.group(), '%Y-%m-%d %H:%M:%S')
                        timestamps.append(ts)
                    except ValueError:
                        pass  # Invalid timestamp format, skip

                if 'ERROR' in line_upper:
                    levels['ERROR'] += 1
                    # Extract message after ERROR
                    parts = line_upper.split('ERROR', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            actual_msg = actual_msg.strip()
                            actual_msg = ' '.join(actual_msg.split())  # normalize whitespace
                            sources[source] += 1
                            messages[actual_msg] += 1
                        else:
                            msg = ' '.join(msg.split())
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
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            actual_msg = actual_msg.strip()
                            actual_msg = ' '.join(actual_msg.split())  # normalize whitespace
                            sources[source] += 1
                            messages[actual_msg] += 1
                        else:
                            msg = ' '.join(msg.split())
                            messages[msg] += 1
                elif 'INFO' in line_upper:
                    levels['INFO'] += 1
                    # Extract message after INFO
                    parts = line_upper.split('INFO', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            actual_msg = actual_msg.strip()
                            actual_msg = ' '.join(actual_msg.split())  # normalize whitespace
                            sources[source] += 1
                            messages[actual_msg] += 1
                        else:
                            msg = ' '.join(msg.split())
                            messages[msg] += 1
                elif 'DEBUG' in line_upper:
                    levels['DEBUG'] += 1
                    parts = line_upper.split('DEBUG', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            sources[source] += 1
                elif 'CRITICAL' in line_upper:
                    levels['CRITICAL'] += 1
                    parts = line_upper.split('CRITICAL', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            sources[source] += 1
                elif 'TRACE' in line_upper:
                    levels['TRACE'] += 1
                    parts = line_upper.split('TRACE', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            sources[source] += 1
                elif 'FATAL' in line_upper:
                    levels['FATAL'] += 1
                    parts = line_upper.split('FATAL', 1)
                    if len(parts) > 1:
                        msg = parts[1].strip()
                        if ':' in msg:
                            source, actual_msg = msg.split(':', 1)
                            source = source.strip()
                            sources[source] += 1

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Get top repeated messages
    top_messages = sorted(messages.items(), key=lambda x: x[1], reverse=True)[:5]

    # Compute timestamp range
    earliest_timestamp = min(timestamps) if timestamps else None
    latest_timestamp = max(timestamps) if timestamps else None

    return {
        'total_lines': total_lines,
        'levels': levels,
        'top_messages': top_messages,
        'earliest_timestamp': earliest_timestamp.isoformat() if earliest_timestamp else None,
        'latest_timestamp': latest_timestamp.isoformat() if latest_timestamp else None,
        'top_sources': sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]
    }

def print_summary(summary):
    """Print the analysis summary to stdout."""
    print("Log Summary")
    print("-----------")
    print(f"Total lines processed: {summary['total_lines']}")
    print(f"Errors: {summary['levels']['ERROR']}")
    print(f"Warnings: {summary['levels']['WARNING']}")
    print(f"Info: {summary['levels']['INFO']}")
    print(f"Debugs: {summary['levels']['DEBUG']}")
    print(f"Criticals: {summary['levels']['CRITICAL']}")
    print(f"Traces: {summary['levels']['TRACE']}")
    print(f"Fatals: {summary['levels']['FATAL']}")
    print()
    if summary['earliest_timestamp']:
        print(f"Earliest timestamp: {summary['earliest_timestamp']}")
        print(f"Latest timestamp: {summary['latest_timestamp']}")
    else:
        print("No timestamps found in log.")
    print()
    print("Top Repeated Issues")
    print("-------------------")
    if summary['top_messages']:
        for msg, count in summary['top_messages']:
            print(f"{msg} - {count}")
    else:
        print("No repeated issues found.")
    print()
    print("Top Sources")
    print("-----------")
    if summary['top_sources']:
        for source, count in summary['top_sources']:
            print(f"{source} - {count}")
    else:
        print("No sources found.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    summary = analyze_log(log_file)
    print_summary(summary)

if __name__ == "__main__":
    main()