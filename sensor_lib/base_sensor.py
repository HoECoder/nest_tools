"""Base Sensor, for tpying"""

from copy import deepcopy

class BaseSensor:
    """The Base Sensor, all sensors derive from this"""
    def __init__(self, config):
        self._raw = deepcopy(config)
        self.process_config(config)
    def process_config(self, config):
        raise NotImplementedError("BaseSensor is an ABC")
    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}({repr(self._raw)})"