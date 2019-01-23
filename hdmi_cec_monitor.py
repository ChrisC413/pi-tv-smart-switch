import sched, time
import aiohttp
import pysmartthings
import asyncio
import cec

token = "SMART THINGS TOKEN HERE"
cec.init()
tv_state = False
s = sched.scheduler(time.time, time.sleep)


async def turn_off_light():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices(device_ids=["DEVICE TO TURN OFF ID"])
        light = devices[0]
        result = await light.command("switch", "off")
        assert result == True


def get_tv_state():
    # devices = cec.list_devices()
    tv = cec.Device(0) #Assume TV is first device
    return tv.is_on()


def check_state():
    global tv_state
    new_tv_state = get_tv_state()
    print("tv state:", tv_state)
    print("new tv state:", new_tv_state)
    if new_tv_state != tv_state:
        tv_state = new_tv_state
        if new_tv_state:
            loop.run_until_complete(turn_off_light())

    s.enter(5, 1, check_state)


loop = asyncio.get_event_loop()
check_state()
s.run()
loop.close()
