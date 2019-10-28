import time
import threading

class NonSense(Exception):
    pass

class Sensor:
    config = {}
    thread = None
    min_delay = 0.0
    max_delay = 0.0
    
    def __init__(self,config, min_delay=0.1, max_delay=30):
        print("Sensor constructor")
        self.config = config
        self.min_delay = min_delay
        self.max_delay = max_delay

    def __iter__(self):
        return self

    def __next__(self):
        ts_before = time.time()
        value = self.sense(timestamp=ts_before)
        ts_after = time.time()
        return (ts_before,value,ts_after)
    
    def delay(self):
        frequency = float(self.config["frequency"])
        range = ((self.max_delay-self.min_delay)/2)
        delay = self.min_delay + frequency * range
        return delay
    
    def run(self):
        for item in self:
            print(item)
            time.sleep(self.delay())
    
    def thread(self):
        self.thread = threading.Thread(target=self.run)
        return self.thread
    
    def sense(self):
        raise NonSense
    
    