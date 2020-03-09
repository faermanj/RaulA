from .module import Module
from logging import DEBUG, WARNING, INFO, ERROR
import logging

class Logging(Module):
    FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'

    default_levels = {
        'botocore': INFO,
        's3transfer': INFO,
        'urllib3': INFO,
        'tb_device_mqtt': WARNING,
        'raula.events': INFO,
        'raula.step': INFO,
        'AWSIoTPythonSDK': WARNING,
        'raula': DEBUG,
        'raula.thingsboard': DEBUG,
        'raula.heartbeats': INFO,
        'raula.aws_iot': INFO,
        'raula.ibs_th1': INFO,
        'raula.ble': INFO,
        'raula.step': INFO,
        'raula.agent': DEBUG, 
        'raula.module': INFO,
        'raula.utils': INFO
    }
    
    def init_logging():
        logging.basicConfig(format=Logging.FORMAT)
        for pack, lvl in Logging.default_levels.items():
            logger = logging.getLogger(pack)
            logger.setLevel(lvl)

    def stand(self):
        levels = ["DEBUG","INFO","WARN","ERROR"]
        section = self.section
        for logger_name in section:
            logger_level = section.get(logger_name,"INFO")
            logger = logging.getLogger(logger_name)
            if (logger_level in levels):
                logger.setLevel(logger_level)
                self.logger.info("Log level of [{}] set to [{}] ".format(logger_name,logger_level))
            else:
                #TODO: Don't pass default settings to modules
                self.logger.debug("Can't set level of [{}] to [{}] ".format(logger_name,logger_level))
            
        super().stand()
