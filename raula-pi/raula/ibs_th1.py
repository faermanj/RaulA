from .sensor import Sensor
import logging
import struct
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEManagementError, BTLEDisconnectError, BTLEInternalError
import binascii
import sys
import time


class IBS_TH1(Sensor):
    addr = None
    peripheral = None
    TH1_CHARACTERISTIC_HANDLE=0x002d
        
    def default_delay(self):
        return (15,180,60)
                
    def stand(self):
        self.addr = self.get_config("addr")
        super().stand()
        def hello_th1(peripheral):
            self.info("IBS_TH1 [{}] standing with addr [{}]".format(self.name, self.addr))
        self.with_peripheral(hello_th1)
    
    def skid(self):
        if(self.peripheral):
            self.info("IBS_TH1 [{}] disconnected".format(self.name))
            self.peripheral.disconnect()    
        
    
    
    def readInt16LE(self,val,offset):
        results = struct.unpack_from("<h",val,offset)
        result = results[0]
        return result
    
    def with_peripheral(self,action,retries = 1):
        if (not self.peripheral and self.addr):
            try:
                self.peripheral = Peripheral()
                self.peripheral.connect(self.addr)
                self.debug("IBS_TH1 [{}] connected to [{}]".format(self.name, self.addr))
            except BTLEDisconnectError as ex:
                self.warning("IBS_TH1 [{}] failed to connect to [{}]".format(self.name, self.addr))
                print(ex)
                self.peripheral = None
        if (self.peripheral and action and retries):
            try:
                return action(self.peripheral)
            except (BTLEDisconnectError,BTLEInternalError) as ex:
                self.info("IBS_TH1 [{}] disconnected. Retrying soon.".format(self.name),exc_info=True)
                self.peripheral = None
                time.sleep(5)
                return self.with_peripheral(action, retries - 1)
        else:
            self.warning("IBS_TH1 [{}] unavailable, [{}] action [{}] retries".format(self.name, action is not None, retries))
            return None
    
    def sense(self, timestamp):
        def read_th1(peripheral):
            val = peripheral.readCharacteristic(IBS_TH1.TH1_CHARACTERISTIC_HANDLE)
            val_str =  binascii.b2a_hex(val).decode('utf-8')
            temp = self.readInt16LE(val,0)
            temp = temp / 100.0
            humi = self.readInt16LE(val,2)
            humi = humi / 100.0
            self.debug("IBS_TH1 [{}] => [{}] [{}]c [{}]h".format(self.addr,val_str,temp,humi))
            result = {
                        "temperature": temp,
                        "humidity": humi,
                    }
            return result 
        return self.with_peripheral(read_th1)