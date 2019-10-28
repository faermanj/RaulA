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


class Agent:
    threads = {}
    config = {}
    
    def mod_probe(self,mod_name,mod_obj):
        thread = mod_obj.thread()
        self.threads[mod_name] = thread
        thread.start()
        print("Thread [{}] started".format(mod_name))


    def mod_probe_all(self):
        print("Starting threads")
        self.mod_probe( "heartbeats-1", Hearbeats(self.config))
        self.mod_probe( "heartbeats-2", Hearbeats(self.config, data = "_<3_"))
        self.mod_probe( "picam", Camera(self.config))
        print("{} threads created".format(len(self.threads)))

    def wait_all(self):
        print("Waiting for threads to finish")
        for thread in self.threads.values():
            thread.join()


    def lookup_config(self):
        user_home = Path.home()

        raula_home = user_home / ".raula"
        self.config["raula_home"] = str(raula_home)

        raula_videos = raula_home / "videos"
        self.config["raula_videos"] = str(raula_videos)

        raula_pictures = raula_home / "pictures"
        self.config["raula_pictures"] = str(raula_pictures)
        self.config["zmq_port"] = "5556"
        self.config["frequency"] = "0.5" 
        self.config["running"] = "1"
        print("raula configuration:")
        print(json.dumps(self.config, sort_keys=True, indent=2))
        return self.config
            
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