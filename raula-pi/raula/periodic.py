import time
import threading
import logging
import datetime
import os
from pathlib import Path
from .module import Module

class NonSense(Exception):
    pass

class Periodic(Module):
    thread = None
    min_delay = 0.0
    max_delay = 0.0

    def __init__(self,agent,name,section, min_delay=0.1, max_delay=10):
        super().__init__(agent,name,section)
        self.config = agent.config
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.mod_probe()
    
    def mod_probe(self):
        thread = self.create_thread() 
        self.agent.threads[self.name] = thread
        thread.start()
        logging.info("Thread [{}] started".format(self.name))
    
    def delay(self):
        frequency = 1.0 - float(self.agent.get_default("frequency"))
        range = ((self.max_delay-self.min_delay)/2)
        delay = self.min_delay + frequency * range
        return delay
    
    def step(self):
        logging.debug("Stepping [{}]".format(self.name))
        ts_before = datetime.datetime.now()
        value = self.sense(timestamp=ts_before)
        ts_after = datetime.datetime.now()
        return {
            "before": str(ts_before),
            "value" : value,
            "after" : str(ts_after)
        }
    
    def is_running(self):
        global_running = self.agent.get_default("running") == "1"
        is_running = global_running
        return is_running
    
    
    def run(self):
        while(self.is_running()):
            try:
                if(self.is_working()):
                    footprint = self.step()
                    self.agent.ingest(self,footprint)
                time.sleep(self.delay())
            except KeyboardInterrupt:
                break
        logging.info("Module [{}] ended".format(self.name))       
                
            
    def create_thread(self):
        self.thread = threading.Thread(target=self.run, daemon=True)
        return self.thread
    
    def get_data_path(self):
        raula_data = Path(self.agent.get_default("raula_data"))
        return raula_data

    def get_log_path(self):
        raula_log = Path(self.agent.get_default("raula_log"))
        return raula_log
    
    def get_module_path(self):
        data_path = self.get_data_path() / self.name
        return data_path

    def get_module_log_path(self):
        data_path = self.get_log_path() / self.name
        return data_path
    
    def mk_filename(self,ts,prefix,ext):
        data_path = self.get_module_path()
        data_path / (ts.strftime("%Y/%m/%d/%H/%M"))
        if(not data_path.exists()):
            logging.debug("Creating path [{}]".format(str(data_path)))
            data_path.mkdir(parents=True, exist_ok=True)
        file_ts = ts.strftime("%Y%m%d%H%M%S%f") 
        data_file = data_path / '{}_{}.{}'.format(prefix,file_ts,ext)
        picture_file = str(data_file)
        return picture_file
    
    # Abstract Methods
    
    def is_working(self):
        return True 
    
    def sense(self):
        raise NonSense