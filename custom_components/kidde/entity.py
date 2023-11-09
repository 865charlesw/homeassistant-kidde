"""Entity base class for Kidde HomeSafe."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from kidde_homesafe import KiddeCommand

from .const import DOMAIN
from .const import MANUFACTURER
from .coordinator import KiddeCoordinator


class KiddeEntity(CoordinatorEntity[KiddeCoordinator]):
    """Entity base class."""

    def __init__(
        self,
        coordinator: KiddeCoordinator,
        device_id: int,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.device_id = device_id
        self.entity_description = entity_description

    @property
    def kidde_device(self) -> dict:
        """The device from the coordinator's data."""
        return self.coordinator.data.devices[self.device_id]

    @property
    def unique_id(self) -> str:
        return f"{self.kidde_device['label']}_{self.entity_description.key}"

    @property
    def device_info(self) -> DeviceInfo | None:
        device = self.kidde_device
        return DeviceInfo(
            identifiers={(DOMAIN, device["label"])},
            name=device.get("label"),
            hw_version=device.get("hwrev"),
            sw_version=str(device.get("fwrev")),
            model=device.get("model"),
            manufacturer=MANUFACTURER,
        )

    async def kidde_command(self, command: KiddeCommand) -> None:
        """Send a Kidde command for this device."""
        client = self.coordinator.client
        device = self.kidde_device
        await client.device_command(device["location_id"], device["id"], command)
