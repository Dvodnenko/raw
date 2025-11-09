import socket
import json


def request(*argv):
    
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        client.connect("/tmp/sine.sock")
    except (FileNotFoundError, ConnectionRefusedError):
        yield "Connection error", 1
        return
    
    # don't parse arguments, services do it by themselves
    # using their own parsing strategy (e.g. AKF, SQL etc.)
    client.sendall(json.dumps(argv).encode())
    buffer = ""

    while True:
        chunk = client.recv(4096).decode("utf-8")
        if not chunk:
            break
        buffer += chunk

        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            if message.strip():
                obj = json.loads(message)
                yield obj["message"], obj["status_code"]
