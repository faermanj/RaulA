from .sensor import Sensor
import time
from pathlib import Path

class Camera(Sensor):
    camera = None
    
    def is_working(self):
        try:
            cam = self.get_camera()
            return cam  != None
        except:
            return False
        
    
    def __init__(self,agent,name):
        super().__init__(agent,name)
    
    def get_camera(self):
        if(self.camera):
            return self.camera
        else:
            try:
                from picamera import PiCamera
                self.camera = PiCamera()
                self.camera.resolution = (1920, 1080)
                self.camera.rotation = 180
                time.sleep(2)
                return self.camera
            except:
                return None
                
        
    def sense(self,timestamp):
        picture_file = self.mk_filename(timestamp,"picam","jpg")
        self.get_camera().capture(picture_file, format = "jpeg")
        return None
    
    #TODO: close camera after use
            