from .sensor import Sensor

class Hearbeats(Sensor):
    data = ""
    
    def __init__(self,config = {}, data = "<3"):
        super().__init__(config)
        print("Heartbeats Constructor")
        self.data = data
        
    def sense(self, timestamp):
        return self.data