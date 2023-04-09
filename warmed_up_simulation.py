import pandas as pd
from heapq import heappop
from collections import deque

from simulation import *


class warm_simulation(simulation):
    def run(self, N):
        """Run simulation.

        Parameters
        ==========
        N: int
            How many times to run the simulation for 1000 calls.
        """

        # Initialise simulation with first call initiation event.
        self.new_call_initiation().schedule(self.FEL)
        warmup_n = 500
        N += warmup_n

        while self.total_calls < N:
            # Restart counters after warm up period.
            if self.total_calls == warmup_n:
                self.blocked = 0
                self.dropped = 0

            _, event = heappop(self.FEL)
            self.clock = event.time

            if event.event_type == 0:
                print('initiate')
                self.call_initiation_handler(event)

            elif event.event_type == 1:
                print('handover')
                self.call_handover_handler(event)
            
            elif event.event_type == 2:
                print('terminate')
                self.call_termination_handler(event)

            print(self.free_channels)

        print(f'Blocked calls: {self.blocked}')
        print(f'Dropped calls: {self.dropped}')
        print(f'Total calls: {self.total_calls-warmup_n}')

        return self.blocked, self.dropped


    def call_handover_handler(self, event):
        """Call handover event handler."""

        self.free_channels[event.station] += 1
        
        if (0 <= event.station + event.direction < 20):

            event.station += event.direction
            
            if self.free_channels[event.station] < 2:
                self.dropped += 1
                print('dropped')
            
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
    

if __name__ == "__main__":
    N = 1000
    blocked_list = deque()
    dropped_list = deque()

    for n in range(N):
        blocked, dropped = warm_simulation().run(N)
        blocked_list.append(blocked)
        dropped_list.append(dropped)
    
    pd.DataFrame(
            {'blocked': blocked_list, 'dropped': dropped_list}
            ).to_csv('warm_simulation_results.csv')