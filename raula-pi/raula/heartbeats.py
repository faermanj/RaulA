from .sensor import Sensor

class Hearbeats(Sensor):
    data = "<3"
    
    def __init__(self,agent,name,section):
        super().__init__(agent,name,section)

        
    def sense(self, timestamp):
        return {
            "heartbeat_data": self.data
        }