import pyautogui as gui
import evdev
import subprocess
import keyboard
import sys
import json
import re

from evdev import UInput, ecodes as e

ui = UInput()

listenmode = False # caps lock pressed, wait for a for sequence start
commandmode = False

deviceList = {}

#deviceNumbers = []
#deviceEvents = []
#deviceNames = []

# read in config
settings = {}

if len(sys.argv) >= 2:
    config_file = sys.argv[1]
    with open(config_file) as json_data_file:
        settings = json.load(json_data_file)
else:
    # assign setting defaults
    settings = {"device_sel_mode":"none", "device":0, "listen_mode":"normal"}
    #settings = {"device_sel_mode":"search", "device":"AT Translated", "listen_mode":"normal"}

print("SETTINGS")
print("--------------")
print("Device selection mode:",settings["device_sel_mode"])
print("Device selection string:",settings["device"])
print("Listen mode:",settings["listen_mode"])
print("--------------")


def grab():
    try:
        device.grab()
        print("GRABBED")
    except: pass

def ungrab():
    try:
        device.ungrab()
        print("UNGRABBED")
    except: pass
    ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 1)
    ui.write(e.EV_KEY, e.KEY_LEFTMETA, 1)
    ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 0)
    ui.write(e.EV_KEY, e.KEY_LEFTMETA, 0)
    ui.syn()

def enter():
    ui.write(e.EV_KEY, e.KEY_ENTER, 1)
    ui.write(e.EV_KEY, e.KEY_ENTER, 0)
    ui.syn()


def getDevices():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        m = re.search("(\d+)", device.fn) # get event input number
        deviceList[m.group(0)] = [device.fn, device.name]

def displayDevices():
    for index in deviceList:
        print(index,"-",deviceList[index])

getDevices()

inputName = ""

# display devices and offer choice to user
if settings["device_sel_mode"] == "none":
    displayDevices()
    choice = input("Enter device number: ")
    inputName = deviceList[choice][0]
elif settings["device_sel_mode"] == "exact":
    deviceInfo = deviceList[str(settings["device"])]
    inputName = deviceInfo[0]
elif settings["device_sel_mode"] == "search":
    for index in deviceList:
        deviceInfo = deviceList[str(index)]
        m = re.search(settings["device"], deviceInfo[1])
        if m: inputName = deviceInfo[0]
    if inputName == "":
        print("ERROR: device",settings["device"],"not found")
        exit()
    
print("Using input device at",inputName)

device = evdev.InputDevice(inputName)
print(device)

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        #print(evdev.categorize(event))
        ke = evdev.KeyEvent(event)
        print(ke.keycode, ke.keystate)

        if not commandmode:
            keys = device.active_keys(True)
            names = [thing[0] for thing in keys]

            if 'KEY_LEFTMETA' in names and 'KEY_RIGHTCTRL' in names:
                print(".........")
                commandmode = True
                ui.write_event(ke)
                ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 0)
                ui.write(e.EV_KEY, e.KEY_LEFTMETA, 0)
                ui.syn()
                grab()
                
        else:
            if ke.keycode == 'KEY_ENTER' and ke.keystate == 0:
                ungrab()
                commandmode = False


            # ---- git commands ----

            # push
            if ke.keycode == 'KEY_DOT' and ke.keystate == 0:
                gui.typewrite("git push origin")
                ungrab()
                commandmode = False
                enter()

            # pull
            if ke.keycode == 'KEY_COMMA' and ke.keystate == 0:
                gui.typewrite("git pull origin")
                ungrab()
                commandmode = False
                enter()
                
            # status
            if ke.keycode == 'KEY_S' and ke.keystate == 0:
                gui.typewrite("git status")
                ungrab()
                commandmode = False
                enter()
                
            # commit
            if ke.keycode == 'KEY_C' and ke.keystate == 0:
                gui.typewrite("git commit -a -m \"\"")
                gui.press('left')
                ungrab()
                commandmode = False
            
ui.close()
