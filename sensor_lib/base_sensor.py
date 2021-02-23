"""Base Sensor, for tpying"""

class BaseSensor:
    """The Base Sensor, all sensors derive from this"""
    def __init__(self, config):
        self.process_config(config)
    def process_config(self, config):
        raise NotImplementedError("BaseSensor is an ABC")