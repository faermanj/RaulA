from .sensor import Sensor
import logging
import struct
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEManagementError, BTLEDisconnectError
import binascii
import sys


class IBS_TH1(Sensor):
    addr = None    
    TH1_CHARACTERISTIC_HANDLE=0x002d
        
    def default_delay(self):
        return (15,180,30)
                
    def stand(self):
        self.addr = self.get_config("addr")
        super().stand()
        self.info("IBS_TH1 [{}] standing with addr [{}]".format(self.name, self.addr))
    
    def readInt16LE(self,val,offset):
        results = struct.unpack_from("<h",val,offset)
        result = results[0]
        return result
    
        # temp_lo_hex = val[b0]
        # temp_hi_hex = val[b1]
        # temp_bytes = bytes([temp_hi_hex,temp_lo_hex])
        # temp_hex = binascii.b2a_hex(temp_bytes).decode('utf-8')
        # temp_int = int(temp_hex, 16)
        # temp_float = temp_int / 100
        # temp_str = str(temp_float)
        # return temp_str
        
    def sense(self, timestamp):
        result = None
        if (self.addr):
                try:
                    peripheral = Peripheral()
                    peripheral.connect(self.addr)
                    val = peripheral.readCharacteristic(IBS_TH1.TH1_CHARACTERISTIC_HANDLE)
                    peripheral.disconnect()
                    val_str =  binascii.b2a_hex(val).decode('utf-8')
                    temp_str = self.readInt16LE(val,0)
                    humi_str = self.readInt16LE(val,2)
                    self.debug("IBS_TH1 [{}] => [{}] [{}]c [{}]h".format(self.addr,val_str,temp_str,humi_str))
                    result = {
                        "temperature_th1": temp_str
                    }
                except BTLEDisconnectError as ex:
                    self.warning("Could not connect to IBS_TH1")
                    self.warning(str(ex))
        else:
            self.error("IBS_TH1 peripheral not found")
        return result