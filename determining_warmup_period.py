import seaborn as sns
import pandas as pd
from collections import deque
from heapq import heappush, heappop
import matplotlib.pyplot as plt

from simulation import *


class single_run_simulation(simulation):
    def __init__(self):

        # Initialise state variables.
        self.clock = 0
        self.FEL = []
        self.free_channels = [10]*20

        # Initialise statistical counters.
        self.blocked = 0
        self.dropped = 0
        self.total_calls = 0

        self.blocked_list = deque()
        self.dropped_list = deque()

        # Maximum likelihood estimators for probability distributions
        self.df = pd.read_excel('simulation_data.xls')
        self.interarrival_mean = self.df['Interarrival time (sec)'].mean()
        self.station_min, self.station_max = 0, 20
        self.duration_mean = self.df['Call duration (sec)'].mean()
        self.speed_mean = self.df['velocity (km/h)'].mean()
        self.speed_std = self.df['velocity (km/h)'].std(ddof=1)
    

    def run(self, N):
        """Run simulation.

        Parameters
        ==========
        N: int
            How many times to run the simulation for 1000 calls.
        """

        # Initialise simulation with first call initiation event.
        self.new_call_initiation().schedule(self.FEL)

        while self.total_calls < N:

            _, event = heappop(self.FEL)
            self.clock = event.time

            if event.event_type == 0:
                self.call_initiation_handler(event)

            elif event.event_type == 1:
                self.call_handover_handler(event)
            
            elif event.event_type == 2:
                self.call_termination_handler(event)

        return self.blocked_list, self.dropped_list


    def call_initiation_handler(self, event):
        """Call initiation event handler."""

        # Schedule new call initiation event.
        self.new_call_initiation().schedule(self.FEL)


        # Update state variables and counters and schedule subsequent events
        self.total_calls += 1

        self.blocked_list.append(self.blocked)
        self.dropped_list.append(self.dropped)

        if self.free_channels[event.station] == 0:
            self.blocked += 1
        
        else:
            self.free_channels[event.station] -= 1

            # Calculate time remaining in current station
            if event.direction == 1:
                time_in_station = 60**2*(2-event.position)/event.speed

            else:
                time_in_station = 60**2*event.position/event.speed
            
            if event.duration < time_in_station:
                event.event_type = 2 # termination event
                event.time = self.clock + event.duration
                event.schedule(self.FEL)
            
            else:
                event.event_type = 1 # handover event
                event.duration -= time_in_station
                event.time = self.clock + time_in_station
                event.schedule(self.FEL)


def plot_warmup(name, data):

    sns.set(style='whitegrid')
    plt.figure()
    sns.lineplot(data)
    plt.xlabel('Total calls')
    plt.ylabel(name)
    plt.savefig('figures/' + name + 'warmup.png')
    plt.show()

if __name__ == "__main__":
    N = 1000
    # N iterations of 2N calls each
    # e.g. run 1000-call simulation 500 times
    
    blocked_list, dropped_list = single_run_simulation().run(N)
    plot_warmup('Cumulative blocked calls', blocked_list)
    plot_warmup('Cumulative dropped calls', dropped_list)