"""The Onemeter PSO integration."""
from __future__ import annotations
from datetime import datetime
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_DEVICE_ID, CONF_API_KEY, CONF_URL, Platform, CONF_NAME)
from .const import (CONF_INFLUXDB_HOST,CONF_INFLUXDB_PORT,CONF_INFLUXDB_DATABASE,CONF_INFLUXDB_USERNAME,CONF_INFLUXDB_PASSWORD)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from .onemeter_reader import OnemeterReader
from .onemeter_reader_detail import OnemeterReaderDetail
from homeassistant.util import dt as dt_util

from .const import COORDINATOR, COORDINATORS, DOMAIN, PLATFORMS, SENSORS, NAME, SCAN_INTERVAL, SCAN_INTERVAL_DETAIL, SCAN_INTERVAL_DETAIL10

import httpx
import logging
import async_timeout
import json

_LOGGER = logging.getLogger(__name__)

from .entity import DummyEntity

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
# PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Onemeter PSO from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    config = entry.data
#    config[CONF_NAME] = "onemeterpso"
    name = config[CONF_NAME]

    shortreading0 = "0"
    shortreading1 = "1"

    onemeter_reader = OnemeterReader(
        config[CONF_URL],
        config[CONF_DEVICE_ID],
        config[CONF_API_KEY],
        async_client=get_async_client(hass),
    )

    onemeter_reader_detail = OnemeterReaderDetail(
        hass,
        config[CONF_URL],
        config[CONF_DEVICE_ID],
        config[CONF_API_KEY],
        config[CONF_INFLUXDB_HOST],
        config[CONF_INFLUXDB_PORT],
        config[CONF_INFLUXDB_DATABASE],
        config.get(CONF_INFLUXDB_USERNAME, None),
        config[CONF_INFLUXDB_PASSWORD],
        shortreading0,
        async_client=get_async_client(hass),
    )

    onemeter_reader_detail10 = OnemeterReaderDetail(
        hass,
        config[CONF_URL],
        config[CONF_DEVICE_ID],
        config[CONF_API_KEY],
        config[CONF_INFLUXDB_HOST],
        config[CONF_INFLUXDB_PORT],
        config[CONF_INFLUXDB_DATABASE],
        config.get(CONF_INFLUXDB_USERNAME, None),
        config[CONF_INFLUXDB_PASSWORD],
        shortreading1,
        async_client=get_async_client(hass),
    )

    _LOGGER.debug("Debug1: %s")
#    _LOGGER.info(hass.config.components)
    _LOGGER.debug(config)
#    _LOGGER.info(HomeAssistant.components.influxdb)

    async def async_update_data():
        """Fetch data from API endpoint."""
        async with async_timeout.timeout(30):
            try:
                await onemeter_reader.getData()
            except httpx.HTTPStatusError as err:
                raise ConfigEntryAuthFailed from err
            except httpx.HTTPError as err:
                raise UpdateFailed(f"Error communicating with API: {err}") from err

            data = {
                description.key: await getattr(onemeter_reader, description.key)()
                for description in SENSORS
            }

            """datetime.now().strftime("%m/%d/%Y, %H:%M:%S")"""
#            data["onemeterdate"] =  await onemeter_reader.onemeterdate()

            _LOGGER.debug("Retrieved data from API %s", data)

            return data

    async def async_update_data_detail():
        """Fetch data from API endpoint."""
        async with async_timeout.timeout(30):
            try:
                await onemeter_reader_detail.getData()
            except httpx.HTTPStatusError as err:
                raise ConfigEntryAuthFailed from err
            except httpx.HTTPError as err:
                raise UpdateFailed(f"Error communicating with API: {err}") from err

            data = {
#                description.key: await getattr(onemeter_reader, description.key)()
#                for description in SENSORS
            }

            """datetime.now().strftime("%m/%d/%Y, %H:%M:%S")"""
#            data["onemeterdate"] =  await onemeter_reader.onemeterdate()

#            _LOGGER.info("Retrieved data from API %s", data)

            return data

    async def async_update_data_detail10():
        """Fetch data from API endpoint."""
        async with async_timeout.timeout(30):
            try:
                await onemeter_reader_detail10.getData()
            except httpx.HTTPStatusError as err:
                raise ConfigEntryAuthFailed from err
            except httpx.HTTPError as err:
                raise UpdateFailed(f"Error communicating with API: {err}") from err

            data = {
#                description.key: await getattr(onemeter_reader, description.key)()
#                for description in SENSORS
            }

            """datetime.now().strftime("%m/%d/%Y, %H:%M:%S")"""
#            data["onemeterdate"] =  await onemeter_reader.onemeterdate()

#            _LOGGER.info("Retrieved data from API %s", data)

            return data

    coordinators: dict[str, DataUpdateCoordinator[any]] = {
      "basic": DataUpdateCoordinator(
          hass,
          _LOGGER,
          name=f"Onemeter {name}",
          update_method=async_update_data,
          update_interval=SCAN_INTERVAL,
      ),
      "detail": DataUpdateCoordinator(
          hass,
          _LOGGER,
          name=f"OnemeterDetail {name}",
          update_method=async_update_data_detail,
          update_interval=SCAN_INTERVAL_DETAIL,
      ),
      "detail10": DataUpdateCoordinator(
          hass,
          _LOGGER,
          name=f"OnemeterDetail10 {name}",
          update_method=async_update_data_detail10,
          update_interval=SCAN_INTERVAL_DETAIL10,
      ),
    }


#    coordinator = DataUpdateCoordinator(
#        hass,
#        _LOGGER,
#        name=f"Onemeter {name}",
#        update_method=async_update_data,
#        update_interval=SCAN_INTERVAL,
#    )


#    coordinatordetail = DataUpdateCoordinator(
#        hass,
#        _LOGGER,
#        name=f"OnemeterDetail {name}",
#        update_method=async_update_data_detail,
#        update_interval=SCAN_INTERVAL_DETAIL,
#    )

    try:
        await coordinators["basic"].async_config_entry_first_refresh()
    except ConfigEntryAuthFailed:
        #onemeter_reader.get_inverters = False
        await coordinators["basic"].async_config_entry_first_refresh()

#    try:
#        await coordinators["detail"].async_config_entry_first_refresh()
#    except ConfigEntryAuthFailed:
        #onemeter_reader.get_inverters = False
#        await coordinators["detail"].async_config_entry_first_refresh()

    try:
        await coordinators["detail10"].async_config_entry_first_refresh()
    except ConfigEntryAuthFailed:
        #onemeter_reader.get_inverters = False
        await coordinators["detail10"].async_config_entry_first_refresh()

#    _LOGGER.info("unique_id %s", entry.unique_id)
#    raise ConfigEntryNotReady(
#        f"Debug"
#      )


    if not entry.unique_id:
        try:
            serial = await onemeter_reader.get_full_serial_number()
            #serial = ''
        except httpx.HTTPError as ex:
            raise ConfigEntryNotReady(
                f"Could not obtain serial number from onemeter: {ex}"
            ) from ex

        _LOGGER.debug("Set Entry Serial %s", serial)
        hass.config_entries.async_update_entry(entry, unique_id=serial)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    _LOGGER.debug("Pred hass.data.setdefault %s %s %s", DOMAIN, entry.entry_id, name)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        COORDINATORS: coordinators,
        NAME: name,
    }
#{
#        COORDINATOR: coordinator,
#        NAME: name,
#    }

    _LOGGER.debug("Pred async forward %s", PLATFORMS)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
