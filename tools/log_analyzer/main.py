from tools.log_analyzer.log_analyzer import LogAnalyzer
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Analyse log files for errors")
    parser.add_argument("method", choices=["read_log", "analyse_errors"])
    parser.add_argument("--file", type=str, help="Path to file log")
    parser.add_argument("--level_index", type=int, help="Which word of the log names the level")
    parser.add_argument("--turn_index", type=int, help="Which word of the log names the turn")
    parser.add_argument("--log_index", type=int, help="Which word of the log names the log/message")
    parser.add_argument("--output", nargs="+", default=["console"], help="Output formats")

    args = parser.parse_args()
    analyzer = LogAnalyzer(args.file if args.file else "dummy.log", args.level_index if args.level_index else None, args.turn_index if args.turn_index else None, args.log_index if args.log_index else None)
    if args.method == "analyse_errors":
        analyzer.analyse_errors(args.output if args.output else ["console"])
    if args.method == "read_log":
        analyzer.read_log()

if __name__ == "__main__":
    main()
