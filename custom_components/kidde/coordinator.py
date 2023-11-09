"""DataUpdateCoordinator for Kidde Homesafe integration."""
import logging
from datetime import timedelta

import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from kidde_homesafe import KiddeClient
from kidde_homesafe import KiddeClientAuthError
from kidde_homesafe import KiddeDataset

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class KiddeCoordinator(DataUpdateCoordinator):
    """Coordinator for Kidde HomeSafe."""

    data: KiddeDataset

    def __init__(self, hass: HomeAssistant, client: KiddeClient) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=30)
        )
        self.client = client

    async def _async_update_data(self) -> KiddeDataset:
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                return await self.client.get_data(get_events=False)
        except KiddeClientAuthError as e:
            raise ConfigEntryAuthFailed from e
        except Exception as e:
            raise UpdateFailed(f"{type(e).__name__} while communicating with API: {e}")
