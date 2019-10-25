import os
import math
import time
import json

from multiprocessing import Process
from pathlib import Path

from .camera import camera_probe


def start_processes(config):
    print("Starting processes")
    processes = {}

    camera_proc = camera_probe(config)
    if (camera_proc):
        processes["camera"] = camera_proc

    print("{} processes created".format(len(processes)))
    for process in processes.values():
        process.start()
    return processes


def wait_all(processes={}):
    print("Waiting for processes to finnish")
    for process in processes.values():
        process.join()


def lookup_config():
    config = {}
    user_home = Path.home()

    raula_home = user_home / ".raula"
    config["raula_home"] = str(raula_home)

    raula_videos = raula_home / "videos"
    config["raula_videos"] = str(raula_videos)

    raula_pictures = raula_home / "pictures"
    config["raula_pictures"] = str(raula_pictures)
    print("raula configuration:")
    print(json.dumps(config, sort_keys=True, indent=2))
    return config


def start():
    print("Starting the ride")
    try:
        config = lookup_config()
        processes = start_processes(config)
        wait_all(processes)
    except KeyboardInterrupt:
        print("Ride stopped")
