from .sensor import Sensor
from sense_hat import SenseHat

# Gyroscope
# Accelerometer
# Magnetometer
# Temperature
# Humidity
# Barometric pressure

class SenseHat(Sensor):
    sensehat = SenseHat()
    
    def __init__(self,agent,name, data = "<3"):
        super().__init__(agent,name)
        self.data = data
        
    def sense(self, timestamp):
        sh = self.sensehat
        gyro = sh.get_gyroscope()
        accel = sh.get_accelerometer()
        compass = sh.get_compass()
        temper = sh.get_temperature()
        humidity = sh.get_humidity()
        pressure = sh.get_pressure()

        return {
            "gyroscope_pitch": gyro["pitch"],
            "gyroscope_roll": gyro["roll"],
            "gyroscope_yaw": gyro["yaw"],
            "acceleration_pitch": accel["pitch"],
            "acceleration_roll": accel["roll"],
            "acceleration_yaw": accel["yaw"],
            "compass": compass,
            "temperature": temper,
            "humidity" : humidity,
            "pressure": pressure
        }