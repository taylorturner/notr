# notr

A minimal command-line journaling and note-logging tool with timestamped entries. Designed for fast, frictionless logs with intuitive slash commands for power users.

---

## 🚀 Features

- Log notes with automatic ISO timestamps
- Continuous input mode (`-c`) for live journaling
- Slash commands for editing, deleting, and reviewing entries
- Stores logs in `~/.notr/logs/YYYY_MM.log`
- Filter logs by date, search terms, or tags
- Export logs to file

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/notr.git
   cd notr
   ```
2. Make it executable:
   ```bash
   chmod +x main.py
   ```
3. (Optional) Set up a `notr` command:
   ```bash
   ./setup.sh
   ```

---

## 🛠 Usage

### Basic Help
```bash
notr -h
```

### Log Continuously
```bash
notr -c
```

Use slash commands:
- `/edit` — Edit the last log entry
- `/delete` — Delete the last log entry
- `/list` — Show last 10 entries
- `/list 20` — Show last 20 entries
- `/help` — Show available commands
- `/q` — Quit continuous mode

### View Logs
```bash
notr -l                      # Show logs from the last 24 hours
notr -l --since 2025-04-01   # Show logs since a specific date
notr -l --search deploy      # Filter by keyword
notr -l --tag meeting        # Filter by tag
notr -l --export out.md      # Export to file
```

---

## 📁 File Structure
- Logs saved to: `~/.notr/logs/YYYY_MM.log`
- Each line is timestamped: `[YYYY-MM-DD HH:MM] Your note here`
- Edited lines are marked: `[YYYY-MM-DD HH:MM] (edit) Updated note`

---

## 🧠 Ideas for Future Enhancements
- Full-text search in `/search` command
- Tags autocomplete or colorizing
- Multi-line entry support
- Log compression/archive by month

---

## 📜 License
GPL-3.0

