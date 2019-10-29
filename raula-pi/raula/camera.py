from .sensor import Sensor
from picamera import PiCamera
import time
from pathlib import Path

class Camera(Sensor):
    camera = None
    
    def __init__(self,agent,name):
        camera = PiCamera()
        camera.resolution = (1920, 1080)
        camera.start_preview()
        self.camera = camera
        time.sleep(2)
        super().__init__(agent,name)
        
    def sense(self,timestamp):
        picture_file = self.mk_filename(timestamp,"picam","jpg")
        self.camera.capture(picture_file)
        return str(picture_file)