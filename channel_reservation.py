import pandas as pd
from simulation import simulation, event
from collections import deque


class channel_reservation_simulation(simulation):
    
    def call_initiation_handler(self, event):
        """Call initiation event handler."""

        # Update state variables and counters and schedule subsequent events
        self.total_calls += 1

        if self.free_channels[event.station] < 2: # want to reserve one
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
            ).to_csv('channel_reservation_simulation_results.csv')