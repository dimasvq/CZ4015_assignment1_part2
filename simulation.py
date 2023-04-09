import pandas as pd
import csv
from numpy.random import exponential, randint, normal, uniform, choice
from heapq import heappush, heappop
from collections import deque


class simulation():

    def __init__(self):

        # Initialise state variables.
        self.clock = 0
        self.FEL = []
        self.free_channels = [10]*20

        # Initialise statistical counters.
        self.blocked = 0
        self.dropped = 0
        self.total_calls = 0

        # Maximum likelihood estimators for probability distributions
        self.df = pd.read_excel('simulation_data.xls')
        self.interarrival_mean = self.df['Interarrival time (sec)'].mean()
        self.station_min, self.station_max = 0, 20
        self.duration_mean = self.df['Call duration (sec)'].mean()
        self.speed_mean = self.df['velocity (km/h)'].mean()
        self.speed_std = self.df['velocity (km/h)'].std(ddof=1)


    def new_call_initiation(self):
        """Create new call initiation event."""

        event_type = 0
        station = randint(self.station_min, self.station_max)
        duration = exponential(self.duration_mean)
        speed = normal(self.speed_mean, self.speed_std)
        position = uniform(low=0, high=2) # car position within cell
        direction = choice([-1,1])
        time = self.clock + exponential(self.interarrival_mean)
        return event(time, event_type, station, duration,
                     speed, position, direction)


    def call_initiation_handler(self, event):
        """Call initiation event handler."""

        # Update state variables and counters and schedule subsequent events
        self.total_calls += 1

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

        # Schedule new call initiation event.
        event = self.new_call_initiation()
        event.schedule(self.FEL)


    def call_handover_handler(self, event):
        """Call handover event handler."""

        # Check if car is exiting the highway
        if (event.station + event.direction < 0 or 
            event.station + event.direction > 19):
            event.event_type = 2 # termination event
            event.time = self.clock
            event.schedule(self.FEL)
        
        else:
            self.free_channels[event.station] += 1
            event.station += event.direction
            
            if self.free_channels[event.station] == 0:
                self.dropped += 1
            
            else:
                self.free_channels[event.station] -= 1
                time_in_station = 60**2*2/event.speed

                if event.duration < time_in_station:
                    event.event_type = 2 # termination event
                    event.time = self.clock + event.duration
                    event.schedule(self.FEL)
                
                else:
                    event.time = self.clock + time_in_station
                    event.duration -= time_in_station
                    event.schedule(self.FEL) # new handover event


    def call_termination_handler(self, event):
        """Call termination event handler."""
        self.free_channels[event.station] += 1
    

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

        print(f'Blocked calls: {self.blocked}')
        print(f'Dropped calls: {self.dropped}')
        print(f'Total calls: {self.total_calls}')

        return self.blocked, self.dropped

        

class event():

    def __init__(self, time, event_type, station, duration, speed, position, direction):
        self.time = time
        self.event_type = event_type
        self.station = station
        self.duration = duration
        self.speed = speed
        self.position = position
        self.direction = direction
    

    def schedule(self, FEL):
        heappush(FEL, (self.time, self))



if __name__ == "__main__":
    N = 500
    blocked_list = deque()
    dropped_list = deque()

    # N iterations of 2N calls each
    # e.g. run 1000-call simulation 500 times
    for n in range(N):
        blocked, dropped = simulation().run(2*N)
        blocked_list.append(blocked)
        dropped_list.append(dropped)
    
    pd.DataFrame(
            {'blocked': blocked_list, 'dropped': dropped_list}
            ).to_csv('simulation_results.csv')
