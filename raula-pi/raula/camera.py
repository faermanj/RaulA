# Raspbery pi camera module
import time
from multiprocessing import Process


def camera_probe(config):
    print("Probing for raspi camera")
    try:
        import picamera
        print("Raspi camera found")
        return Process(target=camera_process, args=(config,))
    except ModuleNotFoundError:
        print("Raspi camera not found")
        return None


def camera_process(config):
    print("Camera Starting")
    import picamera
    video_length = 30
    with picamera.PiCamera() as camera:
        time.sleep(2)  # camera wakeup
        try:
            while(True):
                ts = int(time.time())
                print("click {}".format(ts))
                # TODO mkdir first
                camera.start_recording(
                    '../videos/picam_{}.h264'.format(ts))
                camera.capture(
                    '../pictures/picam_{}.jpg'.format(ts), use_video_port=True)
                # TODO Record faster as accidents may be a glimpse
                camera.wait_recording(video_length)
                camera.stop_recording()
        except KeyboardInterrupt:
            print("Camera Interrupted")
            camera.stop_recording()
