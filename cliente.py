import socket

UDP_PORT = 5005
UDP_IP = "127.0.0.1"
number = 4
MESSAGE = {'text': "hello there!",
           'id': number}

print('Alvo: {}:{}'.format(UDP_IP, UDP_PORT))
print(MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bytes(MESSAGE, 'utf-8'), (UDP_IP, UDP_PORT))
