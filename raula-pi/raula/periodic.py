import time
import threading
import logging
import datetime
import os
from pathlib import Path

class NonSense(Exception):
    pass

class Periodic:
    config = {}
    thread = None
    min_delay = 0.0
    max_delay = 0.0

    def __init__(self,agent,name = "periodic" , min_delay=0.1, max_delay=10):
        self.agent = agent
        self.config = agent.config
        self.name = name
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.mod_probe()
    
    def mod_probe(self):
        thread = self.create_thread() 
        self.agent.threads[self.name] = thread
        thread.start()
        logging.info("Thread [{}] started".format(self.name))

    def __iter__(self):
        return self

    def __next__(self):
        return self.step()
    
    def delay(self):
        frequency = 1.0 - float(self.config["frequency"])
        range = ((self.max_delay-self.min_delay)/2)
        delay = self.min_delay + frequency * range
        return delay
    
    def step(self):
        ts_before = datetime.datetime.now()
        value = self.sense(timestamp=ts_before)
        ts_after = datetime.datetime.now()
        return {
            "before": str(ts_before),
            "value" : value,
            "after" : str(ts_after)
        }
    
    def run(self):
        for item in self:
            self.agent.ingest(self,item)
            time.sleep(self.delay())
    
    def create_thread(self):
        self.thread = threading.Thread(target=self.run)
        return self.thread
    
    def sense(self):
        raise NonSense
    
    def get_data_path(self):
        raula_data = Path(self.config["raula_data"])
        return raula_data
    
    def get_module_path(self):
        data_path = self.get_data_path() / self.name
        return data_path
    
    def mk_filename(self,ts,prefix,ext):
        data_path = self.get_module_path()
        data_path / (ts.strftime("%Y/%m/%d/%H/%M"))
        if(not data_path.exists()):
            print("Creating "+str(data_path))
            data_path.mkdir(parents=True, exist_ok=True)
        file_ts = ts.strftime("%Y%m%d%H%M%S%f")
        data_file = data_path / '{}_{}.{}'.format(prefix,file_ts,ext)
        picture_file = str(data_file)
        print("Offering "+ picture_file)
        return picture_file