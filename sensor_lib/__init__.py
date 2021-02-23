"""Sensor Library"""

from sensor_lib.base_sensor import BaseSensor
from sensor_lib.thermostat import Thermostat

CLASS_FOR_SENSOR_TYPE = {
    "sdm.devices.types.THERMOSTAT": Thermostat,
    "sdm.devices.types.DOORBELL": None,
    "sdm.devices.types.CAMERA": None,
    "sdm.devices.types.DISPLAY": None
}
