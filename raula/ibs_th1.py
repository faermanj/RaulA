from .sensor import Sensor
import logging
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEManagementError
import binascii
import sys

class ScanDelegate(DefaultDelegate):
    logger = logging.getLogger("raula.ble")
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
       if isNewDev:
            self.logger.debug("Discovered device [{}]".format(dev.addr))
       elif isNewData:
            self.logger.debug("Received new data from [{}]".format(dev.addr))

class IBS_TH1(Sensor):
    peripheral = None
    TH1_CHARACTERISTIC_HANDLE=0x002d
            
    def stand(self):
        super().stand()
        self.info("IBS_TH1 Started")

    def ble_scan(self):
        peripheral = None
        try:
            scanner = Scanner().withDelegate(ScanDelegate())
            devices = scanner.scan(10.0)
            addr = self.get_config("addr")
            for dev in devices:
                self.debug("BLE Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                for (adtype, desc, value) in dev.getScanData():
                    self.debug(" [{}] = [{}] ".format(desc, value))
                    is_ibs_th1 = (desc == "Complete Local Name") and (value == "sps")
                    if (is_ibs_th1):
                        addr = dev.addr
            if(addr):
                self.info("BLE IBS_TH1 found at [{}] ".format(addr))
                peripheral = Peripheral(deviceAddr=addr)
            else:
                self.info("BLE IBS_TH1 not found")
        except BTLEManagementError:
            self.warning("Failed to connect to bluetooth peripheral. (BLE scan requires root)")
        except:
            self.error("Unexpected error:")
            self.error(sys.exc_info()[0])
            raise
        return peripheral
    
    def get_peripheral(self):
        if(not self.peripheral):
            self.peripheral = self.ble_scan()
        return self.peripheral

    def is_working(self):
        return self.get_peripheral() != None
        
    def sense(self, timestamp):
        result = None
        peripheral = self.get_peripheral()
        if (peripheral):
            val = self.peripheral.readCharacteristic(IBS_TH1.TH1_CHARACTERISTIC_HANDLE)
            val_str =  binascii.b2a_hex(val).decode('utf-8')
            temp_lo_hex = val[0]
            temp_hi_hex = val[1]
            temp_bytes = bytes([temp_hi_hex,temp_lo_hex])
            temp_hex = binascii.b2a_hex(temp_bytes).decode('utf-8')
            temp_int = int(temp_hex, 16)
            temp_float = temp_int / 100
            temp_str = str(temp_float)
            self.debug("[{}] => [{}] => [{}]".format(handle,val_str,temp_str))
            result = {
                "temperature_th1": temp_str
            }
        return result