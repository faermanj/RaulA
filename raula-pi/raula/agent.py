import os
import sys
import math
import time
import json
import threading
import logging
from logging import DEBUG, WARNING, INFO, ERROR
import random
import configparser

from pathlib import Path

from .heartbeats import Heartbeats
from .camera import Camera
from .sensehat import SenseHat
from .aws_s3 import S3Sync
from .thingsboard import ThingsBoardPublisher
from .utils import to_json,get_raula_home
from .ibs_th1 import IBS_TH1


class Agent():
    events_logger = logging.getLogger('raula.events')
    logger = logging.getLogger('raula.agent')
    
    levels = {
        'botocore': INFO,
        's3transfer': INFO,
        'urllib3': INFO,
        'tb_device_mqtt': WARNING,
        'raula.events':INFO,
        'raula.step':INFO,
        'raula.thingsboard': INFO
    }

    modules = {}
    event_handlers = {}
    config = configparser.ConfigParser()

    def mod_probe(self,mod_name, mod_section):
        module = None
        if (mod_name == "heartbeats"):
            module = Heartbeats()
        elif (mod_name == "picamera"):
            module = Camera() 
        elif (mod_name == "sensehat"):
            module = SenseHat()
        elif (mod_name == "aws_s3"):
            module = S3Sync()
        elif (mod_name == "thingsboard"):
            module = ThingsBoardPublisher()
        elif (mod_name == "ibs_th1"):
            module = IBS_TH1()            
        else:
            self.logger.warning("Module [{}] not found".format(mod_name))
        if(module):
            module.name = mod_name
            module.section = mod_section
            module.agent = self
            self.modules[mod_name] = module
            module.stand()
        return module

    def stand_all(self):
        self.logger.info("Starting Modules")
        sections = self.config.sections()
        for section_name in sections:
            logging.info("Loading module [{}]".format(section_name))
            mod_name = section_name
            mod_section = self.config[section_name]
            module = self.mod_probe(mod_name,mod_section)
    
    def skid_all(self):
        self.logger.debug("Stopping modules")
        for module in self.modules.values():
            logging.debug("Waiting for module [{}] to stop".format(module.name))
            module.skid()

    def join_all(self):
        self.logger.debug("Waiting for modules to join")
        for module in self.modules.values():
            self.logger.debug("Waiting for module [{}] to join".format(module.name))
            module.join()

    # TODO: Proper wait/notify using threading.Event
    def interrupt_all(self):
        self.set_default("running","0")
        self.skid_all()
    
    # TODO: Load config from file with reasonable defaults
    def get_default(self,config_key):
        return self.config.get('DEFAULT',config_key)
    
    def set_default(self,config_key,config_value):
        self.logger.debug("[{}] := [{}]".format(config_key,config_value))
        self.config['DEFAULT'][config_key] = config_value

    def lookup_config(self):
        logging.basicConfig(level=logging.DEBUG)
        raula_home = get_raula_home()
        
        self.set_default("raula_home",str(raula_home))
        self.set_default("raula_data",str( raula_home / "data"))
        self.set_default("raula_log",str( raula_home / "log"))
        self.set_default("frequency","0.5")
        self.set_default("running","1")
        self.set_default("min_delay","0.1")
        self.set_default("max_delay","10")
        
        raula_ini = raula_home / "raula.ini"
        if (raula_ini.exists()):
            try: 
                self.config.read(str(raula_ini),encoding='utf-8-sig')
                self.logger.info("Configuration lodaded [{}]".format(raula_ini))
            except:
                self.logger.error("Configuration error in [{}]".format(raula_ini))
        
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
            event_handler(event)
     
        self.events_logger.debug("Event [{}] handled".format(event_type))
        
    def init_logging(self):
        for pack, lvl in Agent.levels.items():
            logging.getLogger(pack).setLevel(lvl)
        
    def start(self):
        self.logger.info("Raula is starting")
        self.init_logging()
        try:
            self.lookup_config()
            self.stand_all()
            self.join_all()
        except KeyboardInterrupt:
            logging.info("Skidding for KeyboardInterrupt")
            self.interrupt_all()
        self.logger.info("Raula stopped")
    

def start():
    Agent().start()