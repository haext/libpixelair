"""PixelAir Device API.

The PixelAirDevice class is the primary interface, allowing a user to
control any pixelair product, including the Fluora, Fluora Mini, & Monos.
"""

import asyncio
import json
import logging

from aiocoap import *
from datetime import datetime

class PixelAirDevice:
    """Abstraction of a PixelAir device.

    This class provides methods to control e.g. power, etc. of the device.
    """

    def __init__(
        self,
        ip_address: str,
        protocol
    ) -> None:
        """Initialize this device.
        
        Args:
            ip_address: The IP address of the device.
        """
        self._logger = logging.getLogger(f"pixelair.device.ip_address")
        self._ip_address = ip_address
        self._request_id = 0
        
        self._protocol = protocol

    @classmethod
    async def create(
        cls,
        ip_address: str
    ):
        """Asynchronous factory method."""
        protocol = await Context.create_client_context()
        return cls(ip_address=ip_address, protocol=protocol)

    # =========================================================================
    # Controls
    # =========================================================================

    async def turn_on(self) -> None:
        """Turn on the device."""
        await self._set_power(True)

    async def turn_off(self) -> None:
        """Turn off the device."""
        await self._set_power(False)

    async def set_power(self, power: bool) -> None:
        """Set the power state of the device."""
        await self._set_power(power)

    async def _set_power(self, power: bool) -> None:
        self._logger.info("Set power to %s - Attempting", "ON" if power else "OFF")
        await self._send_command(code=POST, type="parameter", payload={
            "id": "phnzVG",
            "value": power
        })
        self._logger.info("Set power to %s - Complete", "ON" if power else "OFF")

    async def _send_command(self, code: Code, type: string, payload) -> None:
        request_id = self._request_id
        self._request_id += 1
        
        payload_extended = {
            "protocol": "1.1",
            "type": type,
            "method": code.name_printable,
            "timestamp": datetime.now().isoformat(),
            "request_id": str(request_id),
            "payload": payload
        }
        payload_string = json.dumps(payload_extended)
        self._logger.info("Sending: %s" % payload_string)
        request = Message(code=code, uri="coap://" + self._ip_address + ":5683/" + type, payload=payload_string.encode('utf-8'))
        
        try:
          response = await self._protocol.request(request).response
        except Exception as e:
          self._logger.error("Failed to send command: %s" % e)
        else:
          self._logger.info("Command result: %s (%r)" % (response.code, response.payload))
