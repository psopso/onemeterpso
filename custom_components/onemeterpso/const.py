"""Constants for the Onemeter PSO integration."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import Platform, UnitOfEnergy, UnitOfPower, UnitOfTemperature
from typing import Final
from datetime import timedelta

DOMAIN = "onemeterpso"
PLATFORMS = [Platform.SENSOR]
COORDINATOR = "coordinator"
COORDINATORS = "coordinators"
NAME = "name"
SCAN_INTERVAL = timedelta(seconds=3600)         #zatim taky kazdou hodinu
SCAN_INTERVAL_DETAIL = timedelta(seconds=86400)  #kazdy den jednou
SCAN_INTERVAL_DETAIL10 = timedelta(seconds=600)  #kazdych 10 minut

DATE_KEY="onemeterdate"
THIS_MONTH_KEY="onemeterthismonth"
PREVIOUS_MONTH_KEY="onemeterpreviousmonth"
DUMMY_KEY="dummy"

SENSORS = (
    SensorEntityDescription(
        key=DATE_KEY,
        name="Datum odectu.",
#        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
#        state_class=SensorStateClass.MEASUREMENT,
#        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key=THIS_MONTH_KEY,
        name="Spotreba tento mesic",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key=PREVIOUS_MONTH_KEY,
        name="Spotreba minuly mesic",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
    ),
)

DUMMYSENSORS = (
    SensorEntityDescription(
        key=DUMMY_KEY,
        name="Dummy",
        entity_registry_visible_default=False,
#        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
#        state_class=SensorStateClass.MEASUREMENT,
#        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)

CONF_INFLUXDB_HOST: Final = "influxdbhost"
CONF_INFLUXDB_PORT: Final = "influxdbport"
CONF_INFLUXDB_DATABASE: Final = "influxdbonemeter"
CONF_INFLUXDB_USERNAME: Final = "influxdbusername"
CONF_INFLUXDB_PASSWORD: Final = "influxdbpassword"
