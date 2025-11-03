import socket
import json


def request(args: list, kwargs: dict, flags: list):
    
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        client.connect("/tmp/raw.sock")
    except (FileNotFoundError, ConnectionRefusedError):
        yield "Connection error", 1
        return

    requestobj = {
        "args": args,
        "kwargs": kwargs,
        "flags": flags,
    }
    
    client.sendall(json.dumps(requestobj).encode())
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
