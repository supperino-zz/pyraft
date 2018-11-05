import random


class Follower:
    def __init__(self):
        self.term = 0
        self.log = []
        self.timeout = random.randint(150, 350)
