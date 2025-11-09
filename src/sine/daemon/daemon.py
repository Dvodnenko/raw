import signal
import socket
import os
import atexit

import setproctitle

from .handler import handlecmd
from .database.session import init_db


SOCKET_PATH = "/tmp/sine.sock"
PID_PATH = "/tmp/sine.pid"
running: bool = True


def cleanup():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    if os.path.exists(PID_PATH):
        os.remove(PID_PATH)

def handle_sigterm(signum, frame):
    global running
    running = False
    print("SIGTERM received, shutting down...")


def run():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)

    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGHUP, handle_sigterm)

    setproctitle.setproctitle("sine")
    atexit.register(cleanup)

    init_db()

    try:
        while running:
            conn, _ = server.accept()
            request = conn.recv(4096).decode()
            if not request:
                conn.close()
                continue

            for row in handlecmd(request):
                conn.sendall(row.encode())
            conn.close()

    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)


if __name__ == "__main__":
    run()
