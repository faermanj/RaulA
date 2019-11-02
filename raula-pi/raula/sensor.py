

from .periodic import Periodic
        
class Sensor(Periodic):
    def __init__(self,agent,name,section):
        super().__init__(agent,name,section)