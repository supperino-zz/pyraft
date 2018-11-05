
class State:
    def __init__(self):
        self.neighboors = {'app2', 'app3'}
        self.timeout = 0
        self.value = 0
        self.term = 0
        self.log = [('Starting', 0)]

        self.uncommited = []

    def switch(self, state):
        self.__class__ = state

    def run(self):
        pass

    def send_heartbeat(self):
        pass
