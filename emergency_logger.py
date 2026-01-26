
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
        
        with open("emergency.log", "a") as f:

            f.write(f"[{turn}] {where}: {type(exception).__name__}: {exception}\n")

    @classmethod
    def upload_to_git(cls, repo_path=".", message="Game played"):

        repo = Repo(repo_path)
        repo.git.add(A=True)
        repo.index.commit(message)
        origin = repo.remote(name="origin")
        origin.push()

    @classmethod
    def log_worker(cls):

        while cls.is_running:
            
            while not cls.loger_queue.empty():
            
                try: 
                    where, exception, game_state = cls.loger_queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                cls.emergency_log(where, exception, game_state)



