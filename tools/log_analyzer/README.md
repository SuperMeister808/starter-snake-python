# Log Analyzer

A CLI tool that parses log entries, analyzes them for critical errors and fallback events. Designed to be used alongside the Battlesnake Game Agent to debug and monitor runtime behavior.

# Features
- log reader that parses log entries into a dictionary with keys like level, turn, message, ... - independent of log format
- error analyzer that iterates through all contents and finds critical errors and fallback events with help of a whitelist
- caches parsed contents as JSON to allow multiple analysis operations without re-reading the log file
- multiple logging handlers like file handler, stream handler, ... - for flexible log output configuration

