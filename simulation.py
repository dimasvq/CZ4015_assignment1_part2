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


    def call_initiation_event(self, event):
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
                event.position = 0
                # In the event of a handover, new cell position will be 0.

            else:
                time_in_station = 60**2*event.position/event.speed
                event.position = 2
                # In the event of a handover, new cell position will be 2.
            
            if event.duration < time_in_station:
                event.event_type = 2 # termination event
                event.time = self.clock + event.duration
                event.shedule(self.FEL)
            
            else:
                event.event_type = 1 # handover event
                event.duration -= time_in_station
                event.time = self.clock + time_in_station


        # Generate new random variables and schedule next call initiation event
        event_type = 0
        station = randint(self.station_min, self.station_max)
        duration = exponential(self.duration_mean)
        speed = normal(self.speed_mean, self.speed_std)
        position = uniform(low=0, high=2) # car position within cell
        direction = choice([-1,1])
        time = self.clock + exponential(self.interarrival_mean)
        event(
            time, event_type, station, duration, speed, position, direction
            ).schedule(self.FEL)


    def call_termination_event(self, event):
        """Call termination event handler."""

        self.free_channels[event.station] += 1


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
    sim = simulation()