import os
import sys
import math
import time
import json
import threading
import logging
import random
import configparser

from pathlib import Path

from .heartbeats import Hearbeats
from .camera import Camera
from .sensehat import SenseHat
from .aws_s3 import S3Sync
from .tb_client import ThingsBoardPublisher
from .utils import to_json,get_raula_home


class Agent:
    threads = {}
    event_handlers = {}
    config = configparser.ConfigParser()

    def mod_probe(self,mod_name, mod_section):
        if (mod_name == "heartbeats"):
            Hearbeats(self,"heartbeats")
        elif (mod_name == "picamera"):
            Camera(self,"picam") 
        elif (mod_name == "sensehat"):
            SenseHat(self,"sense-hat")
        elif (mod_name == "aws_s3"):
            S3Sync(self)
        elif (mod_name == "thingsboard"):
            ThingsBoardPublisher(self)
        else:
            logging.warning("Module [{}] not found".format(mod_name))
            
    def mod_probe_all(self):
        logging.info("Loading Modules")
        sections = self.config.sections()
        for section_name in sections:
            logging.info("Loading module [{}]".format(section_name))
            mod_name = section_name
            mod_section = self.config[section_name]
            module = self.mod_probe(mod_name,mod_section)

    # TODO: Decouple modules from threading
    def wait_all(self):
        logging.debug("Waiting for threads to finish")
        for thread in self.threads.values():
            thread.join()

    # TODO: Load config from file with reasonable defaults
    def get_config(self,config_key):
        return self.config.get('DEFAULT',config_key)
    
    def set_default(self,config_key,config_value):
        logging.debug("[{}] := [{}]".format(config_key,config_value))
        self.config['DEFAULT'][config_key] = config_value

    def lookup_config(self):
        logging.basicConfig(level=logging.DEBUG)
        raula_home = get_raula_home()
        
        self.set_default("raula_home",str(raula_home))
        self.set_default("raula_data",str( raula_home / "data"))
        self.set_default("raula_log",str( raula_home / "log"))
        self.set_default("frequency","0.5")
        self.set_default("running","1")
        
        #TODO: Externalize to file
        self.set_default("aws_bucket_user_data","raula-dev-s3bucket-9qu6t4c2729l")
        self.set_default("raula_uuid","raula-faermanj")
        
        raula_ini = raula_home / "raula.ini"
        if (raula_ini.exists()):
            try: 
                self.config.read(str(raula_ini),encoding='utf-8-sig')
                logging.info("Configuration lodaded [{}]".format(raula_ini))
            except:
                logging.error("Configuration error in [{}]".format(raula_ini))
        
        return self.config

    def ingest(self,sensor,item):
        if(item and item["value"]):
            value = item["value"]
            self.trigger("sensor-data",value)
    
    def on(self,event_type,event_handler):
        event_handlers = self.event_handlers.get(event_type)
        if (not event_handlers):
            event_handlers = []
            self.event_handlers[event_type] = event_handlers
        event_handlers.append(event_handler)
    
    def trigger(self,event_type,event):
        event_handlers = self.event_handlers.get(event_type,{}) 
        for event_handler in event_handlers:
            try:
                event_handler(event)
            except:
                logging.info("failed to handle event [{}]".format(event_type))
        logging.debug("Event [{}] handled".format(event_type))
        
    def init_logging(self):
        logging.getLogger('botocore').setLevel(logging.INFO)
        logging.getLogger('s3transfer').setLevel(logging.INFO)
        logging.getLogger('urllib3').setLevel(logging.INFO)
        logging.getLogger('tb_device_mqtt').setLevel(logging.WARN)

        
    def start(self):
        print("Raula is starting")
        self.init_logging()
        try:
            self.lookup_config()
            self.mod_probe_all()
            self.wait_all()
        except KeyboardInterrupt:
            self.set_default("running","0")
        logging.info("Raula ended")
    

def start():
    Agent().start()