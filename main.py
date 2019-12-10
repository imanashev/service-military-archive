import multiprocessing
import socket
import logging
from dialog import welcome
from database import init_db


PORT = 31337

class Server(object):
    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port

    def start(self):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(100)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=welcome, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", PORT)
    try:
        logging.info("Listening")
        init_db()
        server.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
        logging.info("Closing socket")
        server.socket.close()
        logging.info("All done")