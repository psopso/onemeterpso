"""The base entity for the rest component."""
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.template import Template
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

import logging
_LOGGER = logging.getLogger(__name__)

class DummyEntity(CoordinatorEntity, SensorEntity):
    """A class for entities using DataUpdateCoordinator."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Create the entity that may have a coordinator."""
        self.entity_description = description

        self._attr_entity_registry_visible_default = False
#        self.rest = rest
#        self._resource_template = resource_template
        self._attr_should_poll = not coordinator
#        self._attr_force_update = force_update
        super().__init__(coordinator)

