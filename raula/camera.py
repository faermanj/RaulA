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
        from picamera import PiCamera, PiCameraRuntimeError
        picture_file = self.mk_filename(timestamp,"picam","jpg")
        try:
            self.get_camera().capture(picture_file, format = "jpeg")
        except PiCameraRuntimeError:
            self.warning("Failed to capture camera")
        return None
    
    #TODO: close camera after use
            