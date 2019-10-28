from .sensor import Sensor
from picamera import PiCamera
import time
from pathlib import Path

class Camera(Sensor):
    data = ""
    
    def __init__(self,config = {}):
        super().__init__(config)
        print("Camera Constructor")
        camera = PiCamera()
        camera.resolution = (1920, 1080)
        camera.start_preview()
        self.camera = camera
        time.sleep(2)

        
    def sense(self,timestamp):
        raula_pictures = Path(self.config["raula_pictures"])
        picture_file = str(raula_pictures /  ('picam_{}.jpg'.format(timestamp)))
        self.camera.capture(picture_file)
        return str(picture_file)