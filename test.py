import pyautogui as gui
import time

#gui.typewrite('hello world!')

import evdev
import asyncio


async def print_events(device):
    async for event in device.async_read_loop():
        print(device.fn, evdev.categorize(event), sep=': ')



devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    #print(device.fn, device.name, device.phys, device.capabilities(), "\n\n")
    print(device.fn, device.name, device.phys)
    asyncio.ensure_future(print_events(device))


loop = asyncio.get_event_loop()
loop.run_forever()

