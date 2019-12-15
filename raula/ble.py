from .periodic import Periodic
from .ibs_th1 import IBS_TH1
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEManagementError
import logging
import random
import sys





class BLE(Periodic):
    class ScanDelegate(DefaultDelegate):
        logger = logging.getLogger("raula.ble")
        
        def __init__(self):
            DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                    self.logger.debug("Discovered device [{}]".format(dev.addr))
            elif isNewData:
                    self.logger.debug("Received new data from [{}]".format(dev.addr))
    
    
    def default_delay(self):
        return (30,180,60)
    
    def ble_scan(self):
        try:
            scanner = Scanner().withDelegate(BLE.ScanDelegate())
            devices = scanner.scan(10.0)
            addr = self.get_config("addr")
            for dev in devices:
                self.debug("BLE Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                for (adtype, desc, value) in dev.getScanData():
                    self.debug("    [{}] = [{}] ".format(desc, value))
                    is_ibs_th1 = (desc == "Complete Local Name") and (value == "sps")
                    if (is_ibs_th1):
                        addr = dev.addr            
                        if(addr):
                            self.info("Inkbird TH1 BLE Thermether found at [{}][{}] ".format(dev.addr, dev.addrType))
                            self.agent.mod_probe("ibs_th1", {
                                "guid": "ibs_th1::" + addr,
                                "addr": addr}
                            )
        except BTLEManagementError:
            self.warning("Failed to connect to bluetooth peripheral. (BLE scan requires root)")
        except:
            self.error("Unexpected error:")
            self.error(sys.exc_info()[0])
            raise
    
    def sense(self, timestamp):
        self.info("Starting BLE Scan")
        self.ble_scan()
    
    
 