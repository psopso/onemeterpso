"""Platform for sensor integration."""
from __future__ import annotations
from datetime import datetime, date

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from .const import SENSORS, NAME, DUMMYSENSORS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, COORDINATOR, COORDINATORS
from .entity import DummyEntity

import logging

_LOGGER = logging.getLogger(__name__)

"""def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    # Set up the sensor platform.
    add_entities([OnemeterSensor()])
"""

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data: dict = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: DataUpdateCoordinator = data[COORDINATORS]["basic"]
    onemeter_data: dict = coordinator.data

    onemeter_name: str = data[NAME]
    onemeter_serial_num = config_entry.unique_id

    _LOGGER.debug("Setupentry sensor %s %s %s", onemeter_name, onemeter_serial_num, onemeter_data)
    _LOGGER.debug("********************")

    assert onemeter_serial_num is not None

    """Pokus"""
    entities: list[OnemeterSensor] = []
    for description in SENSORS:
        sensor_data = onemeter_data.get(description.key)
        if isinstance(sensor_data, str) and "not available" in sensor_data:
            continue
        entities.append(
            OnemeterSensor(
               coordinator,
               description,
               onemeter_name,
               onemeter_serial_num,
            )
    )

    async_add_entities(entities, True)

    _LOGGER.debug("AddEntities %s", entities)

    coordinator: DataUpdateCoordinator = data[COORDINATORS]["detail"]
    coordinator10: DataUpdateCoordinator = data[COORDINATORS]["detail10"]
    onemeter_data: dict = coordinator.data
    onemeter_data10: dict = coordinator10.data
    entities: list[DummyEntity] = []
    for description in DUMMYSENSORS:
        sensor_data = onemeter_data.get(description.key)
        if isinstance(sensor_data, str) and "not available" in sensor_data:
            continue
        entities.append(
            DummyEntity(
               coordinator,
               description,
#               onemeter_name,
#               onemeter_serial_num,
    	    )
        )
        entities.append(
            DummyEntity(
               coordinator10,
               description,
#               onemeter_name,
#               onemeter_serial_num,
    	    )
        )

    async_add_entities(entities, True)


    async_add_entities([ExampleSensor()], True)

class OnemeterSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        onemeter_name: str,
        onemeter_serial_num: str,
    ) -> None:
        self.entity_description = description
        self._attr_name = f"{onemeter_name} {description.name}"
        self._attr_unique_id = f"{onemeter_serial_num}_{description.key}"
        self._attr_native_unit_of_measurement = description.native_unit_of_measurement
        self._attr_device_class = description.device_class
        self._attr_state_class = description.state_class
        self._serial_num = onemeter_serial_num

        super().__init__(coordinator)

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
#        if(self._attr_native_value is None):
#          self._attr_native_value = 0
#        else:
#          self._attr_native_value = self._attr_native_value + 1

        self._attr_native_value = _get_data(self,self.coordinator)
    

#    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
#        if(self._attr_native_value is None):
#          self._attr_native_value = 0
#        else:
#          self._attr_native_value = self._attr_native_value + 1

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
#        if(self._attr_native_value is None):
#          self._attr_native_value = 0
#        else:
#          self._attr_native_value =   self._attr_native_value + 1
#
        self._attr_native_value = _get_data(self,self.coordinator)

        self.async_write_ha_state()

class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Example Temperature1"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

#        self._attr_native_value = self.coordinator.data[
#            "onemeterdate"
#        ][self._serial_num]

        if(self._attr_native_value is None):
          self._attr_native_value = 0
        else:
          self._attr_native_value =   self._attr_native_value + 1

def _get_data(onemetersensor,coordinator):
    return onemetersensor.coordinator.data[onemetersensor.entity_description.key]
#     _LOGGER.info("Data: %s", onemetersensor.coordinator.data)
#     raise Exception("Data: %s", onemetersensor.coordinator.data)
