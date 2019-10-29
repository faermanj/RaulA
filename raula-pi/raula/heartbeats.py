from .sensor import Sensor

class Hearbeats(Sensor):
    data = ""
    
    def __init__(self,agent,name, data = "<3"):
        self.data = data
        super().__init__(agent,name)

        
    def sense(self, timestamp):
        return self.data