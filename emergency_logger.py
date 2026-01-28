
import queue

from git import Repo

import time

class EmergencyLogger():
       


    loger_queue = queue.Queue()  

    is_running = False

    last_push = time.time()
        
    push_interval = 300

    worker_thread = None
        
    @classmethod
    def emergency_log(cls, where, exception, game_state):

        turn = game_state.get("turn", "unknown")
        
        try:
            with open("runtime.log", "a") as f:

                f.write(f"[{turn}] {where}: {type(exception).__name__}: {exception}\n")
        except Exception as e:
            raise RuntimeError(f"Could not opne runtime log:{e}")

    @classmethod
    def upload_to_git(cls, repo_path=".", message="Game played", branch="test_runtime_logs"):
        
        repo = Repo(repo_path)
        if repo.active_branch.name != branch:
            raise RuntimeError(f"Refusing to write on branch {repo.active_branch}")
        
        repo.git.add(A=True)
        try:
            repo.git.commit("-m", message, "--allow-empty")
        except Exception as e:
            print(f"No changes to commit or error: {e}")
        
    @classmethod
    def push_to_git(cls, repo_path=".", branch="test_runtime_logs"):    
        repo = Repo(repo_path)
        if repo.active_branch.name != branch:
            raise RuntimeError(f"Could not write on {repo.active_branch.name}")

        origin = repo.remote(name="origin")
        origin.push(branch)

    @classmethod
    def log_worker(cls):

        while cls.is_running:
            
            while not cls.loger_queue.empty():
            
                
                where, exception, game_state = cls.loger_queue.get(timeout=0.1)


                cls.emergency_log(where, exception, game_state)



