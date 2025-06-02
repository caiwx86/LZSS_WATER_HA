"""水费查询集成初始化模块。"""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_SCAN_INTERVAL


from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, CONF_ACCOUNT_NUMBER
from .coordinator import WaterBillDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置水费查询集成。"""
    coordinator = WaterBillDataUpdateCoordinator(
        hass,
        entry.data[CONF_ACCOUNT_NUMBER],
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载水费查询集成。"""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok 