import os
import math
import time
from multiprocessing import Process
from .camera import camera_process

def start_processes():
    print("Starting processes")
    processes = {}
    processes["camera"] = Process(target=camera_process)
    print("{} processes created".format(len(processes)))
    for process in processes.values():
        process.start()
    return processes

def wait_all(processes = {}):
    print("Waiting for processes to finnish")
    for process in processes.values():
        process.join()

def start():
    print("Starting the ride")
    try:
        processes = start_processes()
        wait_all(processes)
    except KeyboardInterrupt:
        print("Ride stopped")