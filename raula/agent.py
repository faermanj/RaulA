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

from pathlib import Path

from .heartbeats import Heartbeats
import importlib
from .utils import to_json, get_raula_home, pip_probe


class Agent():
    events_logger = logging.getLogger('raula.events')
    logger = logging.getLogger('raula.agent')

    levels = {
        'botocore': INFO,
        's3transfer': INFO,
        'urllib3': INFO,
        'tb_device_mqtt': WARNING,
        'raula.events': INFO,
        'raula.step': INFO,
        'AWSIoTPythonSDK': WARNING,
        'raula': INFO,
        'raula.thingsboard': INFO,
        'raula.heartbeats': DEBUG,
        'raula.aws_iot': INFO
    }

    class_names = {
        "heartbeats": (".heartbeats", "Heartbeats"),
        "camera": (".camera", "Camera"),
        "sensehat": (".sensehat", "SenseHat"),
        "aws_s3": (".aws_s3", "S3Sync"),
        "aws_iot": (".aws_iot", "AWSIoTPublisher"),
        "thingsboard": (".thingsboard", "ThingsBoardPublisher"),
        "ibs_th1": (".ibs_th1", "IBS_TH1"),
        "console": (".console", "Console")
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
            module = importlib.import_module(package_name, package="raula")
            if(module):
                clazz = getattr(module, class_name)
                obj = clazz()
                return obj

    def mod_probe(self, mod_name, mod_section={}):
        module = self.load_clazz(mod_name)
        if(module):
            module.name = mod_name
            module.section = mod_section
            module.agent = self
            self.modules[mod_name] = module
            for dep in module.dependencies:
                pip_probe(dep)
            try:
                module.stand()
            except:
                self.logger.warning(
                    "Failed to stand module [{}]".format(mod_name))
        else:
            self.logger.warning("Module [{}] not found".format(mod_name))
        return module

    def stand_all(self):
        self.logger.info("Starting Modules!")
        sections = self.config.sections()
        if (not len(sections)):
            self.mod_probe("heartbeats")
            self.mod_probe("console")
        for section_name in sections:
            logging.info("Loading module [{}]".format(section_name))
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
        for module in self.modules.values():
            self.logger.debug(
                "Waiting for module [{}] to join".format(module.name))
            module.join()

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
        logging.basicConfig(level=logging.DEBUG)
        raula_home = get_raula_home()

        self.set_default("raula_home", str(raula_home))
        self.set_default("raula_data", str(raula_home / "data"))
        self.set_default("raula_log",  str(raula_home / "log"))
        self.set_default("raula_config",  str(raula_home / "config"))
        self.set_default("frequency", "0.5")
        self.set_default("running", "1")
        self.set_default("min_delay", "0.1")
        self.set_default("max_delay", "10")

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
            self.trigger("sensor-data", value)

    def on(self, event_type, event_handler):
        event_handlers = self.event_handlers.get(event_type)
        if (not event_handlers):
            event_handlers = []
            self.event_handlers[event_type] = event_handlers
        event_handlers.append(event_handler)

    def trigger(self, event_type, event):
        event_handlers = self.event_handlers.get(event_type, {})
        for event_handler in event_handlers:
            event_handler(event)

        self.events_logger.debug("Event [{}] handled".format(event_type))

    def init_logging(self):
        for pack, lvl in Agent.levels.items():
            logging.getLogger(pack).setLevel(lvl)
    
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
        self.logger.info("Raula started")

