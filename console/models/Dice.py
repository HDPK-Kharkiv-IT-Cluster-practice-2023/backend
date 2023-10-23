import random


class Dice:
    def __init__(self, min=0, max=100):
        self.min = min
        self.max = max

    def roll_dice(self):
        return random.randint(self.min, self.max)
