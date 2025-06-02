"""水费余额传感器。"""
from __future__ import annotations

from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WaterBillDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置水费余额传感器。"""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WaterBillBalanceSensor(coordinator)])

class WaterBillBalanceSensor(CoordinatorEntity, SensorEntity):
    """水费余额传感器。"""

    def __init__(self, coordinator: WaterBillDataUpdateCoordinator) -> None:
        """初始化传感器。"""
        super().__init__(coordinator)
        self._attr_name = "水费余额"
        self._attr_unique_id = f"{coordinator.account_number}_balance"
        self._attr_native_unit_of_measurement = "元"
        self._attr_icon = "mdi:water"

    @property
    def native_value(self) -> float:
        """返回余额值。"""
        return self.coordinator.data.get("balance", 0.0)

    @property
    def extra_state_attributes(self) -> dict:
        """返回额外状态属性。"""
        return {
            "account_number": self.coordinator.account_number,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } 