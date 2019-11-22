RaulA is a data collector to help the development of IoT solutions. It is a simple python module that will capture data from sensors, cameras and other devices and make it available for further processing, locally or on the cloud. It is designed to be used in a raspberry pi, but any computer with python3 should work out of the box.

# Getting Started
Simply install and run the module:

```bash
$ pip install raula
$ python -m raula
```

Output should be similar to this:
```
INFO:raula.agent:Starting Modules
INFO:raula.periodic:Spinning [heartbeats] at [0.0666] Hz = [15.0054] delay
```

By default RaulA will start the agent with only the heartbeats module.
Add further modules to your raula configuration to build your own solution. 

# Current modules

Sensors:
* SenseHat
* IBS-TH1 thermometer
* GrovePi [WIP]

Cameras:
* Raspi Camera

Cloud:
* ThingsBoard
* AWS S3 
