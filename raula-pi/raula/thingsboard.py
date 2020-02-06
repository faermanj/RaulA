import json
import logging
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from .module import Module
from .utils import to_json

class ThingsBoardPublisher(Module):
    logger = logging.getLogger("raula.thingsboard")
    client = None
    
    def stand(self):
        self.agent.on("sensor-data", self.on_sensor_data)
        self.info("Initializing ThingsBoardPublisher")
        host =  self.get_config("host")
        token = self.get_config("token")
        self.client = TBDeviceMqttClient(host,token)
        self.client.connect()
        self.debug("Connected to thingsboard [{}]".format(host))
        super().stand()
        
    def on_sensor_data(self,event):
        self.debug("Publishing telemtry to thingsboard")
        telemetry = event
        telemetry_json = to_json(telemetry)
        self.debug(telemetry)
        # Sending telemetry and checking the delivery status (QoS = 1 by default)
        success = self.client != None
        if(success):
            result = self.client.send_telemetry(telemetry)
            # get is a blocking call that awaits delivery status  
            success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
        self.logger.debug("Publish to ThingsBoard [successs ? {}]".format(success))
        
        # TODO: Disconnect from ThingsBoard
        # client.disconnect()
