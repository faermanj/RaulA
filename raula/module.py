import logging


class Module:
    agent = None
    name = ""
    section = None
    dependencies = []

    def get_int(self, config_key, default_value=0):
        return int(self.get_config(config_key, default_value))

    def get_float(self, config_key, default_value=0.0):
        return float(self.get_config(config_key, default_value))

    def get_config(self, config_key, default_value=""):
        value = self.section.get(config_key)
        if (not value):
            value = default_value
        return value

    def stand(self):
        self.debug("Module [{}] stand".format(self.name))

    def skid(self):
        self.debug("Module [{}] skid".format(self.name))

    def join(self):
        self.debug("Module [{}] join".format(self.name))

    def getLogger(self):
        return logging.getLogger("raula.{}".format(self.name))

    def debug(self, message):
        self.getLogger().debug(message)

    def info(self, message):
        self.getLogger().info(message)

    def error(self, message):
        self.getLogger().error(message)

    def warning(self, message):
        self.getLogger().warning(message)
