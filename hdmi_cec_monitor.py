import sched, time
import aiohttp
import pysmartthings
import asyncio
import cec
import logging
import config
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logging.info("starting hdmi monitor")

smart_things_token = config.smart_things_token
cec.init()
tv_state = False
schedule = sched.scheduler(time.time, time.sleep)


async def turn_off_light():
    async with aiohttp.ClientSession() as session:
        try:
            api = pysmartthings.SmartThings(session, smart_things_token)
            devices = await api.devices(device_ids=config.device_ids)
            light = devices[0]
            result = await light.command("switch", "off")
            assert result
        except Exception as err:
            logging.warning("Unable to toggle light: " + err)


def get_tv_state():
    # devices = cec.list_devices()
    tv = cec.Device(0)  # Assume TV is first device
    return tv.is_on()


def check_state():
    try:
        global tv_state
        new_tv_state = get_tv_state()
        if new_tv_state != tv_state:
            tv_state = new_tv_state
            if new_tv_state:
                loop.run_until_complete(turn_off_light())
    except Exception as err:
        logging.warning("Failure checking state of CEC: " + err)
    finally:
        schedule.enter(5, 1, check_state)


loop = asyncio.get_event_loop()
check_state()
schedule.run()
loop.close()
logging.error("CEC monitor exiting")
