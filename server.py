from random import randint
import pickle
import socket
import _thread as thread
from states import candidate, follower, leader, state


class Server:

    def __init__(self):
        self.state = follower.Follower()
        self.state.timeout = randint(150, 300)
        self.run()

    def run(self):
        socket.setdefaulttimeout(self.state.timeout/1000)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 8000))
        self.server.listen()

        while True:
            try:
                (clientsocket, address) = self.server.accept()
                message = clientsocket.recv(1024)
                message_type, message_value = pickle.loads(message)

                if message_type == 'PULSE':
                    print('PULSE')
                    value, log, uncommited = message_value
                    if self.state.value != value:
                        print('Updating value to {}'.format(value))
                        self.state.value = value
                    self.log = log
                    self.uncommited = uncommited

                    # se nao for commitado
                    self.state = follower.Follower
                    self.server.settimeout(self.state.timeout/1000)
                    if uncommited:
                        self.state.process_consensus(uncommited, address[0])

                elif message_type == 'VOTE':
                    new_term = message_value
                    if self.state.term != new_term:
                        self.term = new_term
                        print('voting')
                        try:
                            s = socket.socket(
                                socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((address[0], 8001))
                            message = ('1', self.term)
                            s.send(pickle.dumps(message))
                            s.close()
                        except ConnectionRefusedError:
                            pass

            except socket.timeout:
                print('timeout!!')
                if not self.state == leader.Leader:
                    self.state.switch(candidate.Candidate)
                    self.state.run()
                else:
                    self.state.send_heartbeat()


if __name__ == '__main__':
    Server()
