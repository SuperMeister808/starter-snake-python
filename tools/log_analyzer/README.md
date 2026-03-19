# Log Analyzer

A CLI tool that parses log entries, analyzes them for critical errors and fallback events. Designed to be used alongside the Battlesnake Game Agent to debug and monitor runtime behavior.

# Features
- log reader that parses log entries and maps them to keys like level, turn, message, ... — independent of log structure
- error analyzer that iterates through all contents and finds critical errors and fallback events with help of a whitelist
- caches parsed contents as JSON to allow multiple analysis operations without re-reading the log file
- multiple logging handlers like file handler, stream handler, ... - for flexible log output configuration

# Usage

## Install dependencies using pip
Make sure you´ve Python 3.x installed.
```bash
pip install -r requirements.txt
```
## Read the log file
Log entries are split by `|`. Provide indices to map each part to level, turn and message. Note: `--log_index` refers to the message content.
```bash
python -m tools.log_analyzer.main --file file_path --level_index 0 --turn_index 1 --log_index 2
```