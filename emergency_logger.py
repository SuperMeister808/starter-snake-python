
import queue

from git import Repo

import time

from print_collector import PrintCollector

class EmergencyLogger():
       


    loger_queue = queue.Queue()  

    flags = {"is_running": False, "worker_thread": None}

    print_collector = PrintCollector()
        
    @classmethod
    def emergency_log(cls, where, exception, game_state):

        try:
            turn = game_state.get("turn", "unknown")
        except AttributeError as e:
            turn = "unknown"
            print("Game_state must be a dict!")

        try:
            with open("runtime.log", "a") as f:

                f.write(f"[{turn}] {where}: {exception}\n")
        except Exception as e:
            raise RuntimeError(f"Could not opne runtime log:{e}")

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
                    where, exception, game_state = item
                    cls.emergency_log(where, exception, game_state)
                except ValueError as e:
                    print(f"ValueError: {e}")
                    cls.print_collector.collect_message(f"ValueError: {e}")
                    if not isinstance(item, tuple):
                        print("Item is not a tuple!")
                        cls.print_collector.collect_message("Item is not a tuple!")
                    else:
                        if len(item) > 3:
                            print(f"Too many values {item[3:]}")
                            cls.print_collector.collect_message(f"Too many values {item[3:]}")
                        if len(item) < 3:
                            print(f"Not enough values: {item}")
                            cls.print_collector.collect_message(f"Not enough values: {item}")
                    print(f"RAW ITEM:, {item}, {type(item)}")
                    cls.print_collector.collect_message(f"RAW ITEM:, {item}, {type(item)}")
                
                

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





