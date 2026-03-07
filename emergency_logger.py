
import queue

from git import Repo

import time

import logging

from print_collector import PrintCollector
from runtime_logger import RuntimeLogger , DefaultTurnAdapter

class EmergencyLogger():

    runtime_logger = None
    @classmethod
    def setup_runtime_logger(cls, logger_name, logger_file, debug):

        RuntimeLogger.setup(logger_name, logger_file, debug)
        cls.runtime_logger = logging.getLogger(logger_name)
    
    loger_queue = queue.Queue()  

    flags = {"is_running": False, "worker_thread": None}

    print_collector = PrintCollector()

    @classmethod
    def setup(cls, logger):
        cls.runtime_logger = logger
        
    @classmethod
    def emergency_log(cls, where, exception, level=None, turn=None):

        if cls.runtime_logger is None:

            raise RuntimeError("Logger nicht erstellt!")
        
        if level is None:
            level = 40
        if turn is None:
            turn = "unknown"

        try:
            message = cls.create_message(where, exception)
            log = cls.runtime_logger.log(level, message, extra={"turn": turn})
            if log is not None:
                return log
        except Exception as e:
            raise RuntimeError(f"Could not log in runtime log:{e}")
        
    @classmethod
    def create_message(cls, where, exception):

        message = f"{where}: {exception}"
        return message

    @classmethod
    def upload_to_git(cls, repo_path=".", message="Game played", branch="runtime_logs"):
        
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
        repo = Repo(repo_path)
        if repo.active_branch.name != branch:
            raise RuntimeError(f"Could not write on {repo.active_branch.name}")

        origin = repo.remote(name="origin")
        origin.push(branch)
        return {"status": "ok"}

    @classmethod
    def log_worker(cls):
            
            while cls.flags["is_running"] == True or not cls.loger_queue.empty():

                try:
                    item = cls.loger_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                try:
                    where, exception, turn, level = item
                    cls.emergency_log(where, exception, level=level, turn=turn)
                except (ValueError, TypeError) as e:
                    try:
                        where , exception , turn = item
                        cls.emergency_log(where, exception, turn=turn)
                    except (ValueError, TypeError) as e:
                        try:
                            where , exception = item
                            cls.emergency_log(where, exception)
                        except (ValueError, TypeError) as e:

                            cls.emergency_log("log_worker_fallback", e)
                finally:
                    cls.loger_queue.task_done()

    @classmethod
    def clear_emergency_logger(cls):

        cls.flags = {"is_running": False, "worker_thread": None}

        cls.print_collector.clear_messages()

        RuntimeLogger.close_file_handlers(cls.runtime_logger)





