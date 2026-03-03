
from server import Server
from main import ServerHandler

if __name__ == "__main__":

    handler = ServerHandler()
    app = Server({"info": handler.info, "start": handler.start, "end": handler.end, "move": handler.move, "push": handler.push}, 5000)
    app.run_server()