
from server import run_server
import main

if __name__ == "__main__":

    run_server({"info": main.info, "start": main.start, "end": main.end, "move": main.move}, 8001)