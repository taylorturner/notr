#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import os
from pathlib import Path
import re
import sys

BASE_LOG_DIR = Path.home() / ".notr" / "logs"
TIME_FORMAT = "%Y-%m-%d %H:%M"
DATE_INPUT_FORMAT = "%Y-%m-%d"


def ensure_log_dir():
    BASE_LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_log_file_path():
    now = datetime.now()
    file_name = now.strftime("%Y_%m") + ".log"
    return BASE_LOG_DIR / file_name


def log_note(note: str):
    timestamp = datetime.now().strftime(TIME_FORMAT)
    log_file = get_log_file_path()
    entry = f"[{timestamp}] {note.strip()}"
    with open(log_file, "a") as f:
        f.write(entry + "\n")
    sys.stdout.write("\033[F\033[K")
    print(entry)


def edit_last_entry():
    log_file = get_log_file_path()
    if not log_file.exists():
        print("No log file found to edit.")
        return
    with open(log_file, "r") as f:
        lines = f.readlines()
    if not lines:
        print("No entries to edit.")
        return
    last_line = lines[-1]
    print(f"Editing last entry: {last_line.strip()}")
    new_text = input("New text: ").strip()
    if new_text:
        timestamp = datetime.now().strftime(TIME_FORMAT)
        lines[-1] = f"[{timestamp}] (edit) {new_text}\n"
        with open(log_file, "w") as f:
            f.writelines(lines)
        print(f"Updated: {lines[-1].strip()}")


def delete_last_entry():
    log_file = get_log_file_path()
    if not log_file.exists():
        print("No log file found to delete from.")
        return
    with open(log_file, "r") as f:
        lines = f.readlines()
    if not lines:
        print("No entries to delete.")
        return
    removed = lines.pop()
    with open(log_file, "w") as f:
        f.writelines(lines)
    print(f"Deleted: {removed.strip()}")


def list_recent_logs(n=10):
    log_file = get_log_file_path()
    if not log_file.exists():
        print("No log file found.")
        return
    with open(log_file, "r") as f:
        lines = f.readlines()
    print("--- Last entries ---")
    for line in lines[-n:]:
        print(line.strip())


def print_inline_help():
    print("""Commands:
  /edit               Edit the last log entry
  /delete             Delete the last log entry
  /list               Show the last 10 entries
  /list N             Show the last N entries
  /q                  Quit
  /help               Show this help message
""")


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, DATE_INPUT_FORMAT)
    except ValueError:
        print(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
        exit(1)


def read_logs(since=None, search_term=None, tag=None):
    logs = []
    if not BASE_LOG_DIR.exists():
        return logs

    if since is None:
        since = datetime.now() - timedelta(hours=24)

    for file in sorted(BASE_LOG_DIR.glob("*.log")):
        with open(file) as f:
            for line in f:
                if line.startswith("["):
                    try:
                        timestamp_str = line[1:17]
                        timestamp = datetime.strptime(timestamp_str, TIME_FORMAT)
                        if timestamp >= since:
                            if search_term and search_term.lower() not in line.lower():
                                continue
                            if tag and f"#{tag}" not in line:
                                continue
                            logs.append(line.rstrip())
                    except ValueError:
                        continue
    return logs


def export_logs(logs, filepath):
    with open(filepath, "w") as f:
        for line in logs:
            f.write(line + "\n")
    print(f"Logs exported to {filepath}")


def print_help():
    print("""Usage: notr [options]

Options:
  -c                  Start continuous input mode (one log per line, press Ctrl+D to finish)
  -l                  List logs from the past 24 hours
  --since YYYY-MM-DD  Show logs since given date
  --search TEXT       Filter logs by keyword
  --tag TAG           Filter logs by tag (e.g. #deploy)
  --export FILE       Export logs to a file
  -h                  Show this help message

Commands in -c mode:
  /edit               Edit the last log entry
  /delete             Delete the last log entry
  /list               Show the last 10 entries
  /list N             Show the last N entries
  /q                  Quit
  /help               Show this help message
""")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", action="store_true")
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-h", action="store_true")
    parser.add_argument("--since", type=str)
    parser.add_argument("--search", type=str)
    parser.add_argument("--tag", type=str)
    parser.add_argument("--export", type=str)
    args = parser.parse_args()

    ensure_log_dir()

    if args.h or (not args.c and not args.l):
        print_help()
    elif args.c:
        print("Enter log messages. Use /q to quit. Ctrl+D also works.")
        try:
            while True:
                line = input()
                cmd = line.strip()
                if cmd == "/edit":
                    edit_last_entry()
                elif cmd == "/delete":
                    delete_last_entry()
                elif cmd.startswith("/list"):
                    parts = cmd.split()
                    n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
                    list_recent_logs(n)
                elif cmd == "/help":
                    print_inline_help()
                elif cmd == "/q":
                    break
                elif cmd:
                    log_note(cmd)
        except EOFError:
            pass
    elif args.l:
        since = parse_date(args.since) if args.since else None
        logs = read_logs(since=since, search_term=args.search, tag=args.tag)
        for line in logs:
            print(line)
        if args.export:
            export_logs(logs, args.export)


if __name__ == "__main__":
    main()
