
import queue

from git import Repo

import time

import logging

from logger.runtime_logger import RuntimeLogger , DefaultTurnAdapter

# Async logger that processes log entries from a queue in a worker thread.
# Supports variable log entry formats — (where, exception, turn, level) being the most complete.
class EmergencyLogger:

    # class attributes ordered by purpose
    runtime_logger = None
    loger_queue = queue.Queue()
    flags = {"is_running": False, "worker_thread": None}

    @classmethod
    def setup_runtime_logger(cls, logger_name, logger_file, debug):
        # initializes the runtime logger and stores the instance
        RuntimeLogger.setup(logger_name, logger_file, debug)
        cls.runtime_logger = logging.getLogger(logger_name)

    @classmethod
    def setup(cls, logger):
        # sets the runtime logger directly from an existing logger instance
        cls.runtime_logger = logger

    @classmethod
    def emergency_log(cls, where, exception, level=None, turn=None):
        # logs a message to the runtime logger with optional level and turn
        if cls.runtime_logger is None:
            raise RuntimeError("Logger not initialized!")

        if level is None:
            level = 40  # ERROR level
        if turn is None:
            turn = "unknown"

        try:
            message = cls.create_message(where, exception)
            log = cls.runtime_logger.log(level, message, extra={"turn": turn})
        except Exception as e:
            raise RuntimeError(f"Could not log to runtime log: {e}")

    @classmethod
    def create_message(cls, where, exception):
        # formats the log message as "where: exception"
        return f"{where}: {exception}"

    @classmethod
    def upload_to_git(cls, repo_path=".", message="Game played", branch="runtime_logs"):
        # commits all changes to the runtime_logs branch
        repo = Repo(repo_path)
        if repo.active_branch.name != branch:
            raise RuntimeError(f"Refusing to write on branch {repo.active_branch}")
        repo.git.add(A=True)
        try:
            repo.git.commit("-m", message, "--allow-empty")
        except Exception as e:
            raise RuntimeError(f"No changes to commit or error: {e}")

    @classmethod
    def push_to_git(cls, repo_path=".", branch="runtime_logs"):
        # pushes committed logs to the remote repository
        repo = Repo(repo_path)
        if repo.active_branch.name != branch:
            raise RuntimeError(f"Could not write on branch {repo.active_branch.name}")
        origin = repo.remote(name="origin")
        origin.push(branch)
        return {"status": "ok"}

    @classmethod
    def log_worker(cls):
        # processes log entries from the queue until stopped and queue is empty
        while cls.flags["is_running"] or not cls.loger_queue.empty():
            try:
                item = cls.loger_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            try:
                # attempt to unpack in order of most to least complete format
                try:
                    where, exception, turn, level = item
                    cls.emergency_log(where, exception, level=level, turn=turn)
                except (ValueError, TypeError):
                    try:
                        where, exception, turn = item
                        cls.emergency_log(where, exception, turn=turn)
                    except (ValueError, TypeError):
                        try:
                            where, exception = item
                            cls.emergency_log(where, exception)
                        except (ValueError, TypeError) as e:
                            cls.emergency_log("log_worker_fallback", e)
            finally:
                cls.loger_queue.task_done()

    @classmethod
    def clear_emergency_logger(cls):
        # resets flags and closes file handlers after the game ends
        cls.flags = {"is_running": False, "worker_thread": None}
        RuntimeLogger.close_file_handlers(cls.runtime_logger)
