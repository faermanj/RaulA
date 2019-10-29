

from .periodic import Periodic
        
class Sensor(Periodic):
    def __init__(self,agent,name = "sensor", min_delay=0.1, max_delay=30):
        super().__init__(agent,name, min_delay, max_delay)