import logging


class Module:
    logger = logging.getLogger("raula.module")
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

    def set_config(self, config_key, config_value):
        self.section[config_key] = config_value

    def stand(self):
        Module.logger.debug("Module [{}] stand".format(self.name))

    def skid(self):
        Module.logger.debug("Module [{}] skid".format(self.name))

    def join(self):
        Module.logger.debug("Module [{}] join".format(self.name))

    def getLogger(self):
        logger_name = self.name.split("/")[0]
        logger_name = "raula.{}".format(logger_name)
        return logging.getLogger(logger_name)

    def debug(self, *args, **kwargs):
        self.getLogger().debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.getLogger().info(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.getLogger().error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.getLogger().warning(*args, **kwargs)
