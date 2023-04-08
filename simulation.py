import numpy as np
from collections import deque

class simulation():
    def __init__(self):
        # Initialise state variables.
        self.clock = 0
        self.FEL = deque()
        self.free_channels = [10]*20

        # Initialise statistical counters.
        blocked = 0
        dropped = 0
        total_calls = 0
    

    def call_initiation_event(self):
        # self.clock += 





if __name__ == "__main__":
    sim = simulation()