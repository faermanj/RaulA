# Starting Architecture

Date: 2019-10-11

## Status

Accepted

## Context

Initial hardware and software decisions. All this hardware should not be necessary for development, just for runtime. Data for development will be recorded and openly available.

## Decision

### Raspbery Pi

The raspberry pi is inexpensive and easy to get started. The first Raula is a raspberry pi 3, but other models should work just as fine.

### GroveKit

The grove kit offer a series of components that are easy to connect and program, including proximity sensors.

### Python

Python is a simple language with a sane developer experience. Also, most manufaturers and providers offer python bindings to their components, making it a good default option for IoT development.

## Consequences

### Initial Hardware
* [Raspberry Pi](https://www.raspberrypi.org/)
* [Grove Pi](https://www.seeedstudio.com/GrovePi-p-2241.html)
* [TF Mini LiDAR Sensor](https://www.seeedstudio.com/Seeedstudio-Grove-TF-Mini-LiDAR.html)
* [VL53L0X ToF](https://www.seeedstudio.com/Grove-Time-of-Flight-Distance-Sensor-VL53L0-p-3086.html)
* [IMU 10DOF](http://wiki.seeedstudio.com/Grove-IMU_10DOF/)
* [Vibration Motor](https://www.seeedstudio.com/Grove-Vibration-Motor-p-839.html)
* [Night Camera](https://www.amazon.es/gp/product/B0748GQ32H/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
* [Battery Pack](https://www.amazon.es/gp/product/B07KWTS638/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
* [Bike Case](https://www.bike24.com/1.php?content=8;product=319278)

### Initial Software
* [Raspbian for Robots](https://www.dexterindustries.com/raspberry-pi-robot-software/)
* [Python 3](https://www.bike24.com/1.php?content=8;product=319278)
* [GrovePi Python](https://www.dexterindustries.com/GrovePi/programming/python-library-documentation/)
* [PiCamera](https://picamera.readthedocs.io/en/release-1.13/)
  
  

