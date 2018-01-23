import pyautogui as gui
import evdev
import subprocess
import keyboard
import sys
import json
import re
import os





from evdev import UInput, ecodes as e

ui = UInput()

listenmode = False # caps lock pressed, wait for a for sequence start
commandmode = False


mode = "git"

deviceList = {}

# read in config
settings = {}

if len(sys.argv) >= 2:
    statusfile = sys.argv[2] + "/macrokbd/status.dat"
    config_file = sys.argv[1]
    with open(config_file) as json_data_file:
        settings = json.load(json_data_file)
else:
    # assign setting defaults
    settings = {"device_sel_mode":"none", "device":0, "listen_mode":"none"}

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
    if settings["listen_mode"] == "constant": return
    try:
        device.ungrab()
        print("UNGRABBED")
    except: pass
    #ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 1)
    #ui.write(e.EV_KEY, e.KEY_LEFTMETA, 1)
    #ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 0)
    #ui.write(e.EV_KEY, e.KEY_LEFTMETA, 0)
    ui.write(e.EV_KEY, e.KEY_SYSRQ, 1)
    ui.write(e.EV_KEY, e.KEY_SYSRQ, 0)
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


def setStatus(string):
    with open(statusfile, 'w') as sfile:
        sfile.write(string)

def updateStatus():
    statusString = ""
    
    if settings["listen_mode"] == "constant" or commandmode: 
        statusString = "<span color='#00FF00'>ACTIVE"
        #setStatus("<span color='#00FF00'>ACTIVE</span>")
    else:
        statusString = "<span>Listening..."

    statusString += " (" + mode + ")</span>"
    setStatus(statusString)
    

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

if settings["listen_mode"] == "none":
    print("Listen modes")
    print("0 - normal (wait for key combination)")
    print("1 - constant (macro mode always on)")
    choice = input("Select listen mode: ")
    if choice == "0":
        settings["listen_mode"] = "normal"
    elif choice == "1":
        settings["listen_mode"] = "constant"
    else:
        print("ERROR: invalid selection")
        exit()

    
print("Using input device at",inputName)

device = evdev.InputDevice(inputName)
print(device)

if settings["listen_mode"] == "constant": grab()


updateStatus()

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        #print(evdev.categorize(event))
        ke = evdev.KeyEvent(event)
        print(ke.keycode, ke.keystate)

        if not commandmode and settings["listen_mode"] != "constant":
            keys = device.active_keys(True)
            names = [thing[0] for thing in keys]

            #if 'KEY_LEFTMETA' in names and 'KEY_RIGHTCTRL' in names:
            if 'KEY_SYSRQ' in names:
                print(".........")
                commandmode = True
                #updateStatus()
                ui.write_event(ke)
                #ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 0)
                #ui.write(e.EV_KEY, e.KEY_LEFTMETA, 0)
                ui.write(e.EV_KEY, e.KEY_SYSRQ, 0)
                ui.syn()
                grab()
                
        else:
            if ke.keycode == 'KEY_ENTER' and ke.keystate == 0:
                ungrab()
                commandmode = False
                setStatus("Listening...")


            if ke.keycode == 'KEY_ESC' and ke.keystate == 0:
                if mode != "none": 
                    print("Leaving mode '" + mode + "'")
                    mode = "none"
                else: 
                    print("Exiting...")
                    settings["listen_mode"] = "none"
                    commandmode = False
                    ungrab()
                    setStatus("<span color='#999999'>off</span>")
                    exit()


            if mode == "none":
                if ke.keycode == 'KEY_G' and ke.keystate == 0:
                    print("Entering mode 'git'")
                    mode = "git"
                elif ke.keycode == 'KEY_B' and ke.keystate == 0:
                    print("Entering mode 'bash'")
                    mode = "bash"


            # ---- git commands ----
            elif mode == "git":
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

                # add
                if ke.keycode == 'KEY_A' and ke.keystate == 0:
                    gui.typewrite("git add -A")
                    ungrab()
                    commandmode = False
                    enter()

                # log
                if ke.keycode == 'KEY_L' and ke.keystate == 0:
                    gui.typewrite("git log --oneline")
                    ungrab()
                    commandmode = False
                    enter()
                
            # ---- bash commands ----
            elif mode == "bash":
                # push
                if ke.keycode == 'KEY_UP' and ke.keystate == 0:
                    gui.typewrite("cd ..")
                    ungrab()
                    commandmode = False
                    enter()
                    
                if ke.keycode == 'KEY_LEFT' and ke.keystate == 0:
                    gui.typewrite("cd -")
                    ungrab()
                    commandmode = False
                    enter()
                    
                if ke.keycode == 'KEY_DOWN' and ke.keystate == 0:
                    gui.typewrite("cd ~")
                    ungrab()
                    commandmode = False
                    enter()
                    
                if ke.keycode == 'KEY_S' and ke.keystate == 0:
                    gui.typewrite("grep -rl \"\"")
                    gui.press('left')
                    ungrab()
                    commandmode = False

        updateStatus() 
            
ui.close()
