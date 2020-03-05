import os
import sys
import math
import time
import json
import threading
import logging
import argparse
from logging import DEBUG, WARNING, INFO, ERROR
import random
import configparser
import traceback
import uuid

from pathlib import Path

from .heartbeats import Heartbeats
import importlib
from .utils import to_json, get_raula_home, pip_probe


class Agent():
    events_logger = logging.getLogger('raula.events')
    logger = logging.getLogger('raula.agent')

    separator = "/"
    
    levels = {
        'botocore': INFO,
        's3transfer': INFO,
        'urllib3': INFO,
        'tb_device_mqtt': WARNING,
        'raula.events': INFO,
        'raula.step': INFO,
        'AWSIoTPythonSDK': WARNING,
        'raula': DEBUG,
        'raula.thingsboard': DEBUG,
        'raula.heartbeats': INFO,
        'raula.aws_iot': INFO,
        'raula.ibs_th1': INFO,
        'raula.ble': INFO,
        'raula.step': INFO,
        'raula.agent': INFO, 
        'raula.module': INFO 
    }

    class_names = {
        "heartbeats": (".heartbeats", "Heartbeats"),
        "camera": (".camera", "Camera"),
        "sensehat": (".sensehat", "SenseHat"),
        "aws_s3": (".aws_s3", "S3Sync"),
        "aws_iot": (".aws_iot", "AWSIoTPublisher"),
        "thingsboard": (".thingsboard", "ThingsBoardPublisher"),
        "ibs_th1": (".ibs_th1", "IBS_TH1"),
        "console": (".console", "Console"),
        "ble":(".ble","BLE"),
        "ssht":(".ssht","SSHTunnel")
    }

    args = None
    modules = {}
    event_handlers = {}
    config = configparser.ConfigParser()

    def load_clazz(self, mod_name):
        clazz_names = self.class_names.get(mod_name)
        if (clazz_names):
            package_name = clazz_names[0]
            class_name = clazz_names[1]
            self.logger.debug("Importing module [{}] as [{}].[{}]".format(mod_name,package_name,class_name))
            module = None
            try:
                module = importlib.import_module(package_name, package="raula")
                self.logger.debug("Module imported [{}] as [{}].[{}]".format(mod_name,package_name,class_name))            
            except:
                self.logger.debug("Unable to import [{}] as [{}].[{}]".format(mod_name,package_name,class_name),exc_info=True)                            
            if(module is not None):
                clazz = getattr(module, class_name)
                obj = clazz()
                return obj
            else:
                self.logger.debug("Unable to load module [{}] as [{}].[{}]".format(section_name,package_name,class_name))
                
        else:
            self.logger.warning("Could not find class for module [{}] [{}]".format(section_name,mod_name))
        
    def mod_probe(self, section_name, mod_section={}):
        module = None
        guid = None
        section_names = section_name.split("/")
        mod_name = section_names[0]
        if (len(section_names) > 1):
            guid = section_names[1]
        if not guid:
            guid = mod_section.get("guid")
        if not guid:
            guid = str(uuid.uuid4())
        mod_key = "{}{}{}".format(mod_name,Agent.separator,guid)
    
        # Search
        if mod_key in self.modules:
            self.logger.debug("Module [{}] already loaded".format(mod_key))
        else:    
            self.logger.debug("Loading module [{}]/[{}]".format(mod_name,guid))
            try:
                module = self.load_clazz(mod_name)
            except:
                logging.debug("Failed to load module [{}]".format(mod_key),exc_info=True)
                
            if(module):
                module.name = mod_name
                module.guid = guid
                module.section = mod_section
                module.agent = self
                self.modules[mod_key] = module
                for dep in module.dependencies:
                    pip_probe(dep)
                try:
                    module.stand()
                except:
                    self.logger.warning("Failed to stand module [{}]".format(mod_key), exc_info=True)
            else:
                self.logger.warning("Module [{}] not found".format(mod_name))
        return module

    def stand_all(self):
        sections = self.config.sections()
        sections_len = len(sections)
        
        self.logger.debug("Loading [{}] configuration sections".format(sections_len))
        for section_name in sections:
            logging.info("Loading section [{}]".format(section_name))
            mod_name = section_name
            mod_section = self.config[section_name]
            self.mod_probe(mod_name, mod_section)

    def skid_all(self):
        self.logger.debug("Stopping modules")
        for module in self.modules.values():
            logging.debug(
                "Waiting for module [{}] to stop".format(module.name))
            module.skid()

    def join_all(self):
        self.logger.debug("Waiting for modules to join")
        while self.modules:
            mod_key = next(iter(self.modules.keys()))
            mod_obj = self.modules.get(mod_key)
            self.logger.debug(
                "Waiting for module [{}] to join".format(mod_key))
            mod_obj.join()
            del self.modules[mod_key]
        self.logger.debug("All modules finished.")
            

    # TODO: Proper wait/notify using threading.Event
    def interrupt_all(self):
        self.set_default("running", "0")
        self.skid_all()

    # TODO: Load config from file with reasonable defaults
    def get_default(self, config_key):
        return self.config.get('DEFAULT', config_key)

    def set_default(self, config_key, config_value):
        self.logger.debug("[{}] := [{}]".format(config_key, config_value))
        self.config['DEFAULT'][config_key] = config_value

    def lookup_config(self):
        raula_home = get_raula_home()

        self.set_default("raula_home", str(raula_home))
        self.set_default("raula_data", str(raula_home / "data"))
        self.set_default("raula_log",  str(raula_home / "log"))
        self.set_default("raula_config",  str(raula_home / "config"))
        self.set_default("running", "1")

        raula_ini = Path("/boot/raula.ini") 
        
        if not raula_ini.exists():
            raula_ini = raula_home / "raula.ini"

        if (raula_ini.exists()):
            try:
                self.config.read(str(raula_ini), encoding='utf-8-sig')
                self.logger.info(
                    "Configuration lodaded [{}]".format(raula_ini))
            except:
                self.logger.error(
                    "Configuration error in [{}]".format(raula_ini))

        return self.config

    def ingest(self, sensor, item):
        if(item and item["value"]):
            value = item["value"]
            self.trigger("sensor-data", value, sensor)

    def on(self, event_type, event_handler):
        event_handlers = self.event_handlers.get(event_type)
        if (not event_handlers):
            event_handlers = []
            self.event_handlers[event_type] = event_handlers
        event_handlers.append(event_handler)

    def trigger(self, event_type, event, source):
        event_handlers = self.event_handlers.get(event_type, {})
        for event_handler in event_handlers:
            try:
                event_handler(event, source)
                self.events_logger.debug("Event [{}] handled successfully".format(event_type))
            except:
                self.logger.error("Event handler for [{}] crashed".format(event_type),exc_info=True)
        

    def init_logging(self):
        FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
        logging.basicConfig(format=FORMAT)
        for pack, lvl in Agent.levels.items():
            logger = logging.getLogger(pack)
            logger.setLevel(lvl)
            
    
    def init_args(self):
        parser = argparse.ArgumentParser(description='Start the RaulA data collection agent.')
        parser.add_argument("-i", dest="interactive",action='store_true',  help="Start in interactive mode" )
        self.args = parser.parse_args()

    def start(self):
        self.init_args()
        self.init_logging()
        try:
            self.lookup_config()
            self.stand_all()
            if (not self.args.interactive):
                self.join_all()
        except KeyboardInterrupt:
            logging.info("Skidding for KeyboardInterrupt")
            self.interrupt_all()
        self.logger.debug("Raula end of start()")
