
import queue

from git import Repo

import time

import logging

from print_collector import PrintCollector
from runtime_logger import RuntimeLogger , DefaultTurnAdapter


class EmergencyLogger():

    loger_queue = queue.Queue()  

    flags = {"is_running": False, "worker_thread": None}

    print_collector = PrintCollector()

    create_runtime_logger = RuntimeLogger("runtime.log", True)
    runtime_logger = create_runtime_logger.create_runtime_logger()
        
    @classmethod
    def emergency_log(cls, where, exception, level=40, turn="unknown"):

        try:
            message = cls.create_message(where, exception)
            cls.runtime_logger.log(level, message, extra={"turn": turn})
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
            
            while not cls.loger_queue.empty():

                item = cls.loger_queue.get(timeout=0.1)
                try:
                    where, exception, turn, level = item
                    cls.emergency_log(where, exception, level, turn)
                except (ValueError, TypeError) as e:
                    try:
                        where , exception , turn = item
                        cls.emergency_log(where, exception, turn=turn)
                    except (ValueError, TypeError) as e:
                        try:
                            where , exception = item
                        except (ValueError, TypeError) as e:

                            print(f"{e}")

            cls.print_collector.collect_message("logger queue is empty")
                
    @classmethod
    def start_log_worker(cls):

        while cls.flags["is_running"]:

            cls.log_worker()
            time.sleep(0.1)
    
    @classmethod
    def clear_emergency_logger(cls):

        while not cls.loger_queue.empty():

            cls.loger_queue.get(timeout=0.1)

        cls.flags = {"is_running": False, "worker_thread": None}

        cls.print_collector.clear_messages()





