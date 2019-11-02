import json
import logging
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from .module import Module

class ThingsBoardPublisher(Module):
    
    def __init__(self,agent,name,section):
        super().__init__(agent,name,section)
        agent.on("sensor-data", self.on_sensor_data)
        logging.info("Initialized ThingsBoardPublisher with token [{}*]".format(len(self.get_config("token"))))

    def on_sensor_data(self,event):
        telemetry = event
        client = TBDeviceMqttClient("127.0.0.1", self.get_config("token"))
        # Connect to ThingsBoard
        client.connect()
        # Sending telemetry without checking the delivery status
        client.send_telemetry(telemetry) 
        # Sending telemetry and checking the delivery status (QoS = 1 by default)
        result = client.send_telemetry(telemetry)
        # get is a blocking call that awaits delivery status  
        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
        # Disconnect from ThingsBoard
        client.disconnect()
        