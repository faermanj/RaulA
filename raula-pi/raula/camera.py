import time
import picamera

def camera_process():
    print("Camera Starting")
    video_length = 30
    with picamera.PiCamera() as camera:
        time.sleep(2) #camera wakeup 
        try:
            while(True):
                ts = int(time.time())
                print("click {}".format(ts))
                #TODO mkdir first
                camera.start_recording('../videos/picam_{}.h264'.format(ts))
                camera.capture('../pictures/picam_{}.jpg'.format(ts), use_video_port=True)
                #TODO Record faster as accidents may be a glimpse
                camera.wait_recording(video_length)
                camera.stop_recording()
        except KeyboardInterrupt:
            print("Camera Interrupted")
            camera.stop_recording()
