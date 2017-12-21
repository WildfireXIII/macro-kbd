import pyautogui as gui
import evdev
import subprocess
import keyboard

from evdev import UInput, ecodes as e

ui = UInput()

listenmode = False # caps lock pressed, wait for a for sequence start
commandmode = False









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


device = evdev.InputDevice('/dev/input/event0')
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
