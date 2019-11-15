import boto3

from .module import Module
from .utils import to_json
from pathlib import Path


class AWSIoTPublisher(Module):
    iot = boto3.client('iot')
    client = None

    def stand(self):
        self.debug("Standing AWS IoT module")
        endpoint = self.get_endpoint()
        session = boto3.session.Session()
        region_name = session.region_name
        self.debug("Endpoint: {}".format(endpoint))
        self.debug("Client region: {}".format(region_name))
        self.agent.on("sensor-data", self.on_sensor_data)

    def on_sensor_data(self, event):
        self.debug("-- Publishing telemtry to AWS IoT")
        mqtt = self.get_client()
        payload = to_json(event)
        publish_qos = self.get_int("publish_qos", 1)
        raula_uuid = self.get_config("uuid")
        topic_name = "raula/{}".format(raula_uuid)
        # TODO Connection keep-alive
        mqtt.connect()
        mqtt.publish(topic_name, payload, publish_qos)
        mqtt.disconnect()
        self.debug("-- Telemtry published to AWS IoT")

    def get_endpoint(self):
        result = self.iot.describe_endpoint()
        return result["endpointAddress"]

    def get_client(self):
        if(not self.client):
            self.client = self.create_client()
        return self.client

    def create_client(self):
        endpoint_address = self.get_endpoint()
        config_dir = Path(self.get_config("raula_config")) / "aws_iot"
        self.debug("Loading credentials from [{}]".format(str(config_dir)))
        ca_file = config_dir / "verisign-ca.pem.txt"
        private_key = config_dir / "private.pem.key"
        certificate_file = config_dir / "certificate.pem.crt.txt"

        if(not endpoint_address):
            self.error("Endpoint address not found")
        elif(not ca_file.exists()):
            self.error("CA file not found")
        elif(not private_key.exists):
            self.error("PK file not found")
        elif(not certificate_file.exists()):
            self.error("Certificate file not found")
        else:
            ca_file = str(ca_file)
            private_key = str(private_key)
            certificate_file = str(certificate_file)
            from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
            client_id = "raula_{}".format(self.get_config("uuid"))
            mqtt = AWSIoTMQTTClient(client_id)
            mqtt.configureEndpoint(endpoint_address, 8883)
            mqtt.configureConnectDisconnectTimeout(600)
            mqtt.configureCredentials(ca_file, private_key, certificate_file)
            self.debug(
                "MQTT client [{}] created successfully".format(client_id))
            return mqtt
