import time
import socket
import pickle

nodes = {8001, 8002, 8003}
message = 'SIMPLE MESSAGE'

for node in nodes:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.getservbyport(node), 8002))
    s.send(pickle.dumps(message))
    s.close()
