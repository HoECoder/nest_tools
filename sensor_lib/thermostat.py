"""Thermostat Class"""

import time
from enum import Enum
from typing import Mapping

from sensor_lib.base_sensor import BaseSensor

class HVACSetPointModes(Enum):
    Heat = "HEAT"
    Cool = "COOL"
    HeatCool = "HEATCOOL"
    Off = "Off"

class HVACModes(Enum):
    Off = "Off"
    Heating = "HEATING"
    Cooling = "Cooling"

NAME_KEY = "name"
TYPE_KEY = "type"
ASSIGNEE_KEY = "assignee"
TRAITS_KEY = "traits"
TRAITS_INFO_KEY = "sdm.devices.traits.Info"
CUSTOM_NAME_KEY = "customName"
HUMIDITY_KEY = "sdm.devices.traits.Humidity"
AMBIENT_HUMIDITY_KEY = "ambientHumidityPercent"
CONNECTIVITY_KEY = "sdm.devices.traits.Connectivity"
CONNECTIVITY_STATUS_KEY = "status"
FAN_KEY = "sdm.devices.traits.Fan"
FAN_TIMER_MODE_KEY = "timerMode"
THERMOSTAT_MODE_KEY = "sdm.devices.traits.ThermostatMode"
THERMOSTAT_ACTUAL_MODE_KEY = "mode"
AVAILABLE_MODES_KEY = "availableModes"
POSSIBLE_THERMOSTAT_MODES_KEY = "ThermostatMode.availableModes"
ECO_SETTINGS_KEY = "sdm.devices.traits.ThermostatEco"
AVAILABLE_ECO_MODES_KEY = "availableModes"
PSSOBILE_ECO_MODES_KEY = "Eco.availableModes"
ECO_MODE_KEY = "mode"
HEAT_CELSIUS_KEY = "heatCelsius"
COOL_CELSIUS_KEY = "coolCelsius"
THERMOSTAT_HVAC_STATUS_KEY = "sdm.devices.traits.ThermostatHvac"
HVAC_STATUS_KEY = "status"
SETTINGS_KEY = "sdm.devices.traits.Settings"
TEMPERATURE_SCALE_KEY = "temperatureScale"
THERMOSTAT_SETPOINT = "sdm.devices.traits.ThermostatTemperatureSetpoint"
AMBIENT_TEMP_KEY = "sdm.devices.traits.Temperature"
AMBIENT_TEMP_CELSIUS_KEY = "ambientTemperatureCelsius"
PARENT_RELATIONS_KEY = "parentRelations"
PARENT_KEY = "parent"
DISPLAY_NAME_KEY = "displayName"
ECO_HIGH_KEY = "ECO_MODE_HIGH"
ECO_LOW_KEY = "ECO_LOW_KEY"
HEAT_SETPOINT = "Setpoint.Heat"
COOL_SETPOINT = "Setpoint.Cool"
CELSIUS = "CELSIUS"
FAHRENHEIT = "FAHRENHEIT"
TIME_RECEIVED = "time_received"


def celsius_to_fahrenheit(temp: float) -> float:
    return (temp * 9.0/5.0) + 32

def fahrenheit_to_celsius(temp: float) -> float:
    return (temp - 32) * (5.0/9.0)


class Thermostat(BaseSensor):
    def __init__(self, config):
        self._data = None
        super().__init__(config)
    def process_config(self, config) -> Mapping:
        traits = config.get(TRAITS_KEY, {})
        data = {
            NAME_KEY: config.get(NAME_KEY, ''),
            TYPE_KEY: config.get(TYPE_KEY, ''),
            ASSIGNEE_KEY: config.get(ASSIGNEE_KEY, ''),
            TIME_RECEIVED: config.get(TIME_RECEIVED, int(time.time())),
            CUSTOM_NAME_KEY: traits.get(TRAITS_INFO_KEY, {}).get(CUSTOM_NAME_KEY, ''),
            AMBIENT_HUMIDITY_KEY: traits.get(HUMIDITY_KEY, {}).get(AMBIENT_HUMIDITY_KEY, 0),
            CONNECTIVITY_KEY: traits.get(CONNECTIVITY_KEY, {}).get(CONNECTIVITY_STATUS_KEY, "OFFLINE"),
            FAN_KEY: traits.get(FAN_KEY, {}).get(FAN_TIMER_MODE_KEY, "OFF"),
            THERMOSTAT_MODE_KEY: traits.get(THERMOSTAT_MODE_KEY, {}).get(THERMOSTAT_ACTUAL_MODE_KEY, "OFF"),
            POSSIBLE_THERMOSTAT_MODES_KEY: traits.get(THERMOSTAT_MODE_KEY, {}).get(AVAILABLE_MODES_KEY, ["OFF"]),
            ECO_SETTINGS_KEY: traits.get(ECO_SETTINGS_KEY, {}).get(ECO_MODE_KEY, "OFF"),
            PSSOBILE_ECO_MODES_KEY: traits.get(ECO_SETTINGS_KEY, {}).get(AVAILABLE_ECO_MODES_KEY, ["OFF"]),
            ECO_LOW_KEY: traits.get(ECO_SETTINGS_KEY, {}).get(HEAT_CELSIUS_KEY, 0.0),
            ECO_HIGH_KEY: traits.get(ECO_SETTINGS_KEY, {}).get(COOL_CELSIUS_KEY, 0.0),
            TEMPERATURE_SCALE_KEY: traits.get(SETTINGS_KEY, {}).get(TEMPERATURE_SCALE_KEY, "CELSIUS"),
            AMBIENT_TEMP_KEY: traits.get(AMBIENT_TEMP_KEY, {}).get(AMBIENT_TEMP_CELSIUS_KEY, 0.0),
            HVAC_STATUS_KEY: traits.get(THERMOSTAT_HVAC_STATUS_KEY, {}).get(HVAC_STATUS_KEY, "OFF")
        }
        _mode = data[THERMOSTAT_MODE_KEY]
        if _mode == HVACSetPointModes.Heat.value:
            data[HEAT_SETPOINT] = traits.get(THERMOSTAT_SETPOINT, {}).get(HEAT_CELSIUS_KEY, None)
        elif _mode == HVACSetPointModes.Cool.value:
            data[COOL_SETPOINT] = traits.get(THERMOSTAT_SETPOINT, {}).get(COOL_CELSIUS_KEY, None)
        elif _mode == HVACSetPointModes.HeatCool.value:
            data[HEAT_SETPOINT] = traits.get(THERMOSTAT_SETPOINT, {}).get(HEAT_CELSIUS_KEY, None)
            data[COOL_SETPOINT] = traits.get(THERMOSTAT_SETPOINT, {}).get(COOL_CELSIUS_KEY, None)
        self._data = data
    @property
    def device_id(self):
        return self.name.split('/')[-1]
    @property
    def name(self):
        return self._data[NAME_KEY]
    @property
    def device_type(self):
        return self._data[TYPE_KEY]
    @property
    def assignee(self):
        return self._data[ASSIGNEE_KEY]
    @property
    def temp_scale(self):
        return self._data[TEMPERATURE_SCALE_KEY]
    @property
    def ambient_temp_celsius(self):
        if self.temp_scale == CELSIUS:
            return self._data[AMBIENT_TEMP_KEY]
        return fahrenheit_to_celsius(self._data[AMBIENT_TEMP_KEY])
    @property
    def ambient_temp_fahrenheit(self):
        if self.temp_scale == FAHRENHEIT:
            return celsius_to_fahrenheit(self._data[AMBIENT_TEMP_KEY])
        return self._data[AMBIENT_TEMP_KEY]
    @property
    def ambient_temp(self):
        """Gets the ambient temperature in the devices scale"""
        if self.temp_scale == CELSIUS:
            return self.ambient_temp_celsius
        return self.ambient_temp_fahrenheit
    @property
    def ambient_humidity(self):
        return self._data[AMBIENT_HUMIDITY_KEY]
    @property
    def mode(self):
        return self._data[THERMOSTAT_MODE_KEY]
    @property
    def available_modes(self):
        return self._data[POSSIBLE_THERMOSTAT_MODES_KEY]
    @property
    def status(self):
        return self._data[HVAC_STATUS_KEY]
    @property
    def connectivity(self):
        return self._data[CONNECTIVITY_KEY]
    @property
    def eco_mode(self):
        return self._data[ECO_MODE_KEY]
    @property
    def available_eco_modes(self):
        return self._data[AVAILABLE_ECO_MODES_KEY]
    @property
    def heat_setpoint(self):
        return self._data.get(HEAT_SETPOINT, None)
    @property
    def cool_setpoint(self):
        return self._data.get(COOL_SETPOINT, None)
    @property
    def setpoint(self):
        if self.mode == HVACSetPointModes.Heat.value:
            return self.heat_setpoint
        elif self.mode == HVACSetPointModes.Cool.value:
            return self.cool_setpoint
        elif self.mode == HVACSetPointModes.HeatCool.value:
            return self.heat_setpoint, self.cool_setpoint
    @property
    def setpoint_per_settings(self):
        if self.mode == HVACSetPointModes.Heat.value:
            if self.temp_scale == FAHRENHEIT:
                return celsius_to_fahrenheit(self.heat_setpoint)
            return self.heat_setpoint
        elif self.mode == HVACSetPointModes.Cool.value:
            if self.temp_scale == FAHRENHEIT:
                return celsius_to_fahrenheit(self.cool_setpoint)
            return self.cool_setpoint
        elif self.mode == HVACSetPointModes.HeatCool.value:
            if self.temp_scale == FAHRENHEIT:
                return celsius_to_fahrenheit(self.heat_setpoint), celsius_to_fahrenheit(self.cool_setpoint)
            return self.heat_setpoint, self.cool_setpoint
    @property
    def time_received(self):
        return self._data[TIME_RECEIVED]
