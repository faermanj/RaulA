import logging

class Module:    
    agent = None
    name = ""
    section = None

    def get_config(self,config_key):
        return self.section.get(config_key)

    def stand(self):
        self.debug("Module [{}] stand".format(self.name))

    def skid(self):
        self.debug("Module [{}] skid".format(self.name))

    def join(self):
        self.debug("Module [{}] join".format(self.name))
    
    def getLogger(self):
        return logging.getLogger("raula.{}".format(self.name))
    
    def debug(self,message):
        self.getLogger().debug(message)
    def info(self,message):
        self.getLogger().info(message)
    def error(self,message):
        self.getLogger().error(message)
    def warning(self,message):
        self.getLogger().warning(message)