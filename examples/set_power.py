import logging
import asyncio

import libpixelair
import argparse

logging.basicConfig(level=logging.INFO)

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('on', 'true', '1'):
        return True
    elif value.lower() in ('off', 'false', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(description="A sample pixelair control application")
    parser.add_argument("ip_address", type=str, help="The IPv4 address of the pixelair device.")
    parser.add_argument("power", type=str_to_bool, help="The power state to set.")
    args = parser.parse_args()
    asyncio.run(set_power(args.ip_address, args.power))

async def set_power(ip_address: str, power: bool):
    device = await libpixelair.PixelAirDevice.create(ip_address)
    await device.set_power(power)

if __name__ == "__main__":
    main()
