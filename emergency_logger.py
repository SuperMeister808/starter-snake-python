
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
    def emergency_log(cls, where, exception, level, turn="unknown"):

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

                try:
                    item = cls.loger_queue.get(timeout=0.1)
                    where, exception, turn, level = item
                    cls.emergency_log(where, exception, level, turn)
                except (ValueError, TypeError) as e:
                    print(f"ValueError: {e}")
                    cls.print_collector.collect_message(f"ValueError: {e}")
                    if not isinstance(item, (tuple, list)):
                        print("Item is not a tuple or a list!")
                        cls.print_collector.collect_message("Item is not a tuple or a list!")
                    else:
                        if len(item) > 4:
                            print(f"Too many values: {item[3:]}")
                            cls.print_collector.collect_message(f"Too many values: {item[3:]}")
                        if len(item) < 4:
                            print(f"Not enough values: {item}")
                            cls.print_collector.collect_message(f"Not enough values: {item}")
                    print(f"RAW ITEM:, {item}, {type(item)}")
                    cls.print_collector.collect_message(f"RAW ITEM:, {item}, {type(item)}")

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





