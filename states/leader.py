from .state import State
import socket
import pickle


class Leader(State):
    def __init__(self, *args, **kwargs):
        pass

    def send_heartbeat(self):
        for node in self.neighboors:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_ip = socket.gethostbyname(node)
            s.connect((host_ip, 8000))
            message = ('PULSE', (self.value, self.log, self.uncommited))
            s.send(pickle.dumps(message))
            s.close()

    def wait_consensus(self):
        print('Waiting consensus')
        consensus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        consensus_socket.settimeout(None)

        try:
            consensus_socket.bind(('', 8003))
        except:
            consensus_socket.close()
            consensus_socket.bind(('', 8003))

        consensus_socket.listen()

        confirmations = 1

        while confirmations <= len(self.neighboors)//2:
            (clientsocket, address) = consensus_socket.accept()
            confirmations += 1

        if confirmations > len(self.neighboors)//2:
            for log in self.uncommited:
                self.log.append(log)
            print('Consensus reached. Changing self.value')
            self.uncommited = []
            self.value += 3
        consensus_socket.close()

    def listen_client(self):
        self.application_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.application_socket.bind(('', 8002))
        self.application_socket.listen()
        self.application_socket.settimeout(None)

        while True:
            (clientsocket, address) = self.application_socket.accept()
            print('Command recieved by application.')
            message = pickle.loads(clientsocket.recv(1024))
            self.uncommited.append((message, self.term))
