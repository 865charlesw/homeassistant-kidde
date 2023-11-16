"""The Kidde HomeSafe integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from kidde_homesafe import KiddeClient

from .const import DOMAIN
from .coordinator import KiddeCoordinator

PLATFORMS: list[Platform] = [
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kidde HomeSafe from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    client = KiddeClient(entry.data["cookies"])
    hass.data[DOMAIN][entry.entry_id] = coordinator = KiddeCoordinator(
        hass, client, update_interval=entry.data["update_interval"]
    )
    await coordinator.async_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
