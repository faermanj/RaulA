import io
import random
import picamera
import json
import os
from datetime import datetime
from pathlib import Path

BUFFER_SECS = 30
EXTRA_SECS = 15


def lookup_app_home():
    home = Path.home()
    app_home = home / '.raula'
    app_home.mkdir(parents=True, exist_ok=True)
    return app_home

def getdir(subpath):
    dir = app_home / subpath
    dir.mkdir(parents=True, exist_ok=True)
    return dir

def now_s():
    start_time = datetime.now()
    start_time_s = start_time.strftime("%d_%m_%Y__%H_%M_%S")
    return start_time_s

def event_detected():
    # Randomly return True (like a fake motion detection routine)
    return 1 # random.randint(0, 10) == 0


def record_picamera():
    camera = picamera.PiCamera()
    stream = picamera.PiCameraCircularIO(camera, seconds=BUFFER_SECS)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if event_detected():
                # Keep recording for 10 seconds and only then write the
                # stream to disk
                camera.wait_recording(EXTRA_SECS)
                fname =  'event_'+now_s()+'.h264'
                fname_s = str(videos_dir / fname)
                print("Writing event to {}".format(fname_s))
                stream.copy_to(fname_s)
    finally:
        camera.stop_recording()



app_home = lookup_app_home()
videos_dir = getdir('videos')

config = {
    'app_home': str(app_home),
    'videos_dir': str(videos_dir),
    'event_detected': 0
}

def start():
    print("Pedalar e suave!")
    config_s = json.dumps(config)
    print(config_s)
    record_picamera()