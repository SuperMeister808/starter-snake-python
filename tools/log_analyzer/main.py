from tools.log_analyzer.log_analyzer import LogAnalyzer
import argparse

def main():
    parser = argparse.ArgumentParser(description="Analyse log files for errors")
    parser.add_argument("method", choices=["read_log", "analyse_errors"])
    parser.add_argument("--file", type=str, default=r"C:\Users\emilc\AppData\Local\game_agent\starter-snake-python\logs\runtime.log", help="Path to file log")
    parser.add_argument("--file_handler", type=str, default=r"C:\Users\emilc\AppData\Local\game_agent\starter-snake-python\tools\log_analyzer\log_analyzer.log", help="File handler for output format file")
    parser.add_argument("--level_index", type=int, default=None, help="Which word of the log names the level")
    parser.add_argument("--turn_index", type=int, default=None, help="Which word of the log names the turn")
    parser.add_argument("--log_index", type=int, default=None, help="Which word of the log names the log/message")
    parser.add_argument("--output", nargs="+", default=["console"], help="Output formats")

    args = parser.parse_args()
    analyzer = LogAnalyzer(args.file, args.file_handler, args.level_index, args.turn_index, args.log_index)
    if args.method == "analyse_errors":
        analyzer.analyse_errors(args.output)
    if args.method == "read_log":
        analyzer.read_log()

if __name__ == "__main__":
    main()