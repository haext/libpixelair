import logging
import asyncio

from aiocoap import *
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
    parser.add_argument("ipaddr", type=str, help="The IPv4 address of the pixelair device.")
    parser.add_argument("power", type=str_to_bool, help="The power state to set.")
    args = parser.parse_args()
    asyncio.run(set_power(args.ipaddr, args.power))

async def set_power(ipaddr: str, power: bool):
    protocol = await Context.create_client_context()

    #payload = b"{\"protocol\":\"1.1\",\"type\":\"domain\",\"method\":\"GET\",\"domain\":\"config\",\"timestamp\":\"2026-06-09T17:53:18.160Z\",\"request_id\":1}"
    #request = Message(code=GET, uri="coap://" + ipaddr + "/domain", payload=payload)
    payload = b"{\"protocol\":\"1.1\",\"type\":\"parameter\",\"method\":\"POST\",\"timestamp\":\"2026-06-09T19:26:32.331Z\",\"request_id\":3,\"payload\":{\"id\":\"phnzVG\",\"value\":" + str(power).lower().encode('utf-8') + b"}}"
    request = Message(code=POST, uri="coap://" + ipaddr + ":5683/parameter", payload=payload)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print("Failed to fetch resource:")
        print(e)
    else:
        print("Result: %s\n%r" % (response.code, response.payload))

if __name__ == "__main__":
    main()
