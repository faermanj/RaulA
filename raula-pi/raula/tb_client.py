import json
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

class ThingsBoardPublisher():
    
    def __init__(self,agent):
        agent.on("sensor-data", self.on_sensor_data)

    def on_sensor_data(self,event):
        telemetry = event
        # TODO COnfig 
        token = "MoTecuJcNIV8SQrldGiN"
        client = TBDeviceMqttClient("127.0.0.1", token)
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
        