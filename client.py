import time
import socket
import pickle

nodes = {'server1', 'server2', 'server3'}

time.sleep(15)
message = 'teste'
for node in nodes:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = socket.gethostbyname(node)
    s.connect((host_ip, 8002))
    s.send(pickle.dumps(message))
    s.close()
