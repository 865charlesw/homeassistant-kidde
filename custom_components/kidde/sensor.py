"""Sensor platform for Kidde Homesafe integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import KiddeCoordinator
from .entity import KiddeEntity


_SENSOR_DESCRIPTIONS = (
    SensorEntityDescription("smoke_level", icon="mdi:smoke", name="Smoke Level"),
    SensorEntityDescription("co_level", icon="mdi:molecule-co", name="CO Level"),
    SensorEntityDescription(
        "battery_state", icon="mdi:battery-alert", name="Battery State"
    ),
    SensorEntityDescription("last_seen", icon="mdi:home-clock", name="Last Seen"),
    SensorEntityDescription(
        "last_test_time", icon="mdi:home-clock", name="Last Test Time"
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    coordinator: KiddeCoordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    for device_id in coordinator.data.devices:
        for entity_description in _SENSOR_DESCRIPTIONS:
            sensors.append(
                KiddeSensorEntity(coordinator, device_id, entity_description)
            )
    async_add_devices(sensors)


class KiddeSensorEntity(KiddeEntity, SensorEntity):
    """Sensor for Kidde HomeSafe."""

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.kidde_device.get(self.entity_description.key)
