
import queue

from git import Repo

import time

class EmergencyLogger():
       
    def __init__(self):

        self.loger_queue = queue.Queue()  

        self.is_running = False

        self.last_push = time.time()
        
        self.push_interval = 300


        

    def emergency_log(self, where, exception, game_state):

        turn = game_state.get("turn", "unknown")
        self.emergency = True
        
        with open("emergency.log", "a") as f:

            f.write(f"[{turn}] {where}: {type(exception).__name__}: {exception}\n")

    def upload_to_git(self, repo_path=".", message="Emergency Log Updated"):

        repo = Repo(repo_path)
        repo.git.add(A=True)
        repo.index.commit(message)
        origin = repo.remote(name="origin")
        origin.push()

    def log_worker(self):

        while self.is_running:

            if time.time() - self.last_push >= self.push_interval:

                try:
                    self.upload_to_git()
                except Exception as e:
                    self.emergency_log("git_push", e, {"turn": "unknown"})
            
            try: 
                where, exception, game_state = self.loger_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            self.emergency_log(where, exception, game_state)



