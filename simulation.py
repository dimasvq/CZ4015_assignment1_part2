import pandas as pd
from numpy.random import exponential, randint, normal, uniform, choice
from heapq import heappush, heappop


class simulation():
    def __init__(self):
        # Initialise state variables.
        self.clock = 0
        self.FEL = []
        self.free_channels = [10]*20

        # Initialise statistical counters.
        blocked = 0
        dropped = 0
        total_calls = 0

        # Maximum likelihood estimators for probability distributions
        self.df = pd.read_excel('simulation_data.xls')
        self.interarrival_mean = self.df['Interarrival time (sec)'].mean()
        self.station_min, self.station_max = 0, 20
        self.duration_mean = self.df['Call duration (sec)'].mean()
        self.speed_mean = self.df['velocity (km/h)'].mean()
        self.speed_std = self.df['velocity (km/h)'].std(ddof=1)
    
    def advance_time(self):
        """Time advancement mechanism."""
        self.FEL
         
    

    def call_initiation_event(self, event):
        """Initiation event handler."""
        event_type, station, duration, speed, position, direction = event






        self.total_calls += 1

        # Generate random variables for next call initiation event
        station = randint(self.station_min, self.station_max)
        duration = exponential(self.duration_mean)
        speed = normal(self.speed_mean, self.speed_std)
        position = uniform(low=0, high=2) # car position within cell
        direction = choice([-1,1])

        # Schedule next call initiation event
        self.clock += exponential(self.interarrival_mean)
        self.FEL.append((self.clock, station, duration, speed, position, direction))



        





if __name__ == "__main__":
    sim = simulation()