from .sensor import Sensor

class Heartbeats(Sensor):
    data = "<3"
    
    def sense(self, timestamp):
        return {
            "heartbeat_data": self.data
        }