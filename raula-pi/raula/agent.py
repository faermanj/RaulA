import os
import math
import time
import json
import threading
import logging
import random
from pathlib import Path

from .heartbeats import Hearbeats
from .camera import Camera
from .sensehat import SenseHat
from .aws import S3Sync

class Agent:
    threads = {}
    config = {}
    


    def mod_probe_all(self):
        logging.info("Starting threads")
        # Hearbeats(self,"heartbeats-1")
        # Hearbeats(self,"heartbeats-2", data = "_<3_")
        Camera(self,"picam")
        # SenseHat(self,"sense-hat")
        S3Sync(self)
        
        logging.info("{} threads created".format(len(self.threads)))

    def wait_all(self):
        logging.info("Waiting for threads to finish")
        for thread in self.threads.values():
            thread.join()


    def lookup_config(self):
        logging.basicConfig(level=logging.INFO)

        user_home = Path.home()

        raula_home = user_home / ".raula"
        self.config["raula_home"] = str(raula_home)

        raula_videos = raula_home / "data"
        self.config["raula_data"] = str(raula_videos)
        self.config["frequency"] = "0.5" 
        self.config["running"] = "1"
        
        #TODO: Externalize to file
        self.config["aws_bucket_user_data"] ="raula-dev-s3bucket-9qu6t4c2729l"
        self.config["raula_uuid"] = "raula-faermanj"
        
        print("raula configuration:")
        print(json.dumps(self.config, sort_keys=True, indent=2))
        return self.config


    
    def ingest(self,sensor,item):
        out = json.dumps(item)
        print(out)
            
    def start(self):
        print("Starting the ride")
        try:
            self.lookup_config()
            self.mod_probe_all()
            self.wait_all()
        except KeyboardInterrupt:
            print("Ride stopped")
            
def start():
    Agent().start()    