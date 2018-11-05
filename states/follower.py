from random import randint
import pickle
import socket
from .state import State
from .leader import Leader
from .candidate import Candidate


class Follower(State):
    def __init__(self):
        super().__init__()
        self.timeout = randint(150, 300)

    def process_consensus(self, uncommited, host_ip):
        print('Sending log acceptance')
        processed_actions = set()
        for action in uncommited:
            self.log.append((uncommited, self.term))

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host_ip, 8003))
            message = ('loaded log',)
            s.send(pickle.dumps(message))
            s.close()
        except ConnectionRefusedError:
            pass
