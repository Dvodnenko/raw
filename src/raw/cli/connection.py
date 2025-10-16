import socket
import json


def request(args: list, kwargs: dict, flags: list) -> dict:
    
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        client.connect("/tmp/raw.sock")
    except FileNotFoundError:
        return "raw: daemon is not started"

    requestobj = {
        "args": args,
        "kwargs": kwargs,
        "flags": flags,
    }
    
    client.sendall(json.dumps(requestobj).encode())
    response: dict = json.loads(client.recv(1024).decode())

    return response
