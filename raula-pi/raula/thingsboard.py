import json
import logging
from .module import Module
from .utils import to_json

class ThingsBoardPublisher(Module):
    # dependencies = ["tb-mqtt-client"]
    logger = logging.getLogger("raula.thingsboard")
    client = None
    
    def stand(self):
        from tb_gateway_mqtt import TBGatewayMqttClient

        self.agent.on("sensor-data", self.on_sensor_data)
        self.host =  self.get_config("host")
        self.token = self.get_config("token") 
        self.info("Initializing ThingsBoardPublisher to [{}]".format(self.host))
        self.client = TBGatewayMqttClient(self.host,self.token)
        super().stand()
    
    def skid(self):
        self.client.disconnect()
        super().skid()

    def on_sensor_data(self,event,sensor):
        import time
        from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
        from tb_gateway_mqtt import TBGatewayMqttClient

        self.debug("Publishing telemetry to thingsboard")
        try:
            device_id = sensor.guid
            self.client.connect()
            self.client.gw_connect_device(device_id)
            self.debug("Connected to thingsboard [{}] as [{}]".format(self.host,device_id))
            telemetry =  {"ts": int(round(time.time() * 1000)), 
                          "values": event
                          }    
            success = self.client != None
            if(success):
                result = self.client.gw_send_telemetry(device_id,telemetry)
                # get is a blocking call that awaits delivery status  
                success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
            self.logger.debug("Publish to ThingsBoard [successs ? {}]".format(success))
        except:
            self.error("Failed to connect to thingsboard [{}]".format(self.host),exc_info=True)
        