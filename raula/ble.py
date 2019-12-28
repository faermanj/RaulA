from .periodic import Periodic
from .ibs_th1 import IBS_TH1
from .utils import to_json
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEManagementError, BTLEDisconnectError
import logging
import random
import sys

class BLE(Periodic):
    LOCAL_NAME_ADTYPE = 9
    scanner = None
    
    class ScanDelegate(DefaultDelegate):
        logger = logging.getLogger("raula.ble")
        agent = None
        
        def __init__(self, agent):
            self.agent = agent
            DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                    local_name = dev.getValueText(BLE.LOCAL_NAME_ADTYPE)
                    is_ibs_th1 = local_name == "sps"
                    if (is_ibs_th1):
                        self.logger.info("Inkbird TH1 BLE Thermether found at [{}][{}] ".format(dev.addr, dev.addrType))
                        addr = dev.addr            
                        if(addr):
                            self.agent.mod_probe("ibs_th1", {
                                "guid": addr,
                                "addr": addr}
                            )
                    else:
                        self.logger.debug("Discovered device [{}] [{}]".format(dev.addr, local_name))
                    
            elif isNewData:
                    self.logger.debug("Received new data from [{}]".format(dev.addr))
    
    
    def default_delay(self):
        return (30,600,240)
    
    def stand(self):
        super().stand()
        self.ble_scan()
    
    def ble_scan(self):
        try:
            hci_index = self.get_int("hci_index",0)
            scanner = Scanner(hci_index).withDelegate(BLE.ScanDelegate(self.agent))
            self_delay = self.delay()
            scan_delay = round(self_delay / 4.0, 2)
            self.info("Starting BLE Scan on hci[{}] for [{}]s ".format(hci_index,scan_delay))
            devices = scanner.scan(scan_delay)
        except BTLEManagementError:
            self.warning("Failed to connect to bluetooth peripheral. (BLE scan requires root)")
        except BTLEDisconnectError:
            self.warning("BLE device disconnected")
        except:
            self.error("Unexpected error:")
            self.error(sys.exc_info()[0])
            raise
    
    def sense(self, timestamp):
        self.ble_scan()
    
    
 