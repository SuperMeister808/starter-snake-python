from tools.log_analyzer.log_analyzer import LogAnalyzer
import argparse

# Entry point — parses CLI arguments and routes to the correct analyzer method.
# Run with 'python -m tools.log_analyzer.main --help' to see all available options.
def main():
    # CLI entry point — parses arguments and routes to the correct analyzer method
    parser = argparse.ArgumentParser(description="Analyse log files for critical errors and fallback events")

    parser.add_argument("method", choices=["read_log", "analyse_errors"],
                        help="Operation to perform")
    parser.add_argument("--file", type=str, default=r"C:\Users\emilc\AppData\Local\game_agent\starter-snake-python\logs\runtime.log",
                        help="Path to the log file")
    parser.add_argument("--file_handler", type=str, default=r"C:\Users\emilc\AppData\Local\game_agent\starter-snake-python\tools\log_analyzer\log_analyzer.log",
                        help="Path to the log analyzer output file")
    parser.add_argument("--level_index", type=int, default=0,
                        help="Index of the level field in each log entry")
    parser.add_argument("--turn_index", type=int, default=1,
                        help="Index of the turn field in each log entry")
    parser.add_argument("--log_index", type=int, default=2,
                        help="Index of the message field in each log entry")
    parser.add_argument("--output", nargs="+", default=["console"],
                        help="Output formats — file, console or both")

    args = parser.parse_args()
    analyzer = LogAnalyzer(args.file, args.file_handler, args.level_index, args.turn_index, args.log_index)

    # route to the correct method based on the command argument
    if args.method == "read_log":
        analyzer.read_log()
    if args.method == "analyse_errors":
        analyzer.analyse_errors(args.output)

if __name__ == "__main__":
    main()