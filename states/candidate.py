from .state import State
from .leader import Leader
import socket
import pickle


class Candidate(State):

    def __init__(self):
        super().__init__()

    def run(self):
        self.ask_votes()

    def ask_votes(self):
        self.term += 1
        votes = 1
        vote_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        vote_listen.bind(('', 8001))
        vote_listen.listen()

        for node in self.neighboors:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_ip = socket.gethostbyname(node)
            s.connect((host_ip, 8000))
            message = ('voting', self.term)
            s.send(pickle.dumps(message))
            s.close()

        while votes <= len(self.neighboors)//2:
            try:
                (clientsocket, address) = vote_listen.accept()
            except socket.timeout:
                break
            vote, term = pickle.loads(clientsocket.recv(1024))
            if vote == '1' and term == self.term:
                votes += 1

        vote_listen.close()

        if votes > len(self.neighboors)//2:
            print('Elected. Becoming leader')
            self.switch(Leader)
