
import queue

from git import Repo

class EmergencyLogger():
       
    def __init__(self):

        self.loger_queue = queue.Queue()  

        self.is_running = False        
        

    def emergency_log(self, where, exception, game_state):

        turn = game_state["turn"]
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

        while not self.loger_queue.empty():
            
            where, exception, game_state = self.loger_queue.get()

            self.emergency_log(where, exception, game_state)
            self.upload_to_git()

        self.is_running = False