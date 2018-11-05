import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print(data)

# termo: quando começa a eleição e termina com a falta do lider
# / mensagem : {termo}
# quando um seguidor recebe uma mensagem com um termo
# menor que o seu, ignora esta mensagem
# quando um seguidor recebe uma mensagem com um termo
# maior que o seu, atualiza o termo e torna-se seguidor do
# líder vigente
