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
                ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 1)
                ui.write(e.EV_KEY, e.KEY_LEFTMETA, 1)
                ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 0)
                ui.write(e.EV_KEY, e.KEY_LEFTMETA, 0)
                ui.syn()
                commandmode = False
            





        
'''

        if not listenmode and not commandmode: # wait for caps lock
            if ke.keycode == 'KEY_CAPSLOCK' and ke.keystate == 1:
                listenmode = True


                
        elif listenmode: # caps lock is down
            
            # if a is pressed (sequence to enter command mode)
            if ke.keycode == 'KEY_ESC' and ke.keystate == 1:
                ui.write(e.EV_KEY, e.KEY_ESC, 1)
                ui.write(e.EV_KEY, e.KEY_ESC, 0)
                ui.write(e.EV_KEY, e.KEY_CAPSLOCK, 0)
                ui.syn()
                
                grab()
                
                commandmode = True

            elif ke.keystate != 2: # ignore held down keys
                listenmode = False

                
        elif commandmode:
            if ke.keycode == 'KEY_ENTER' and ke.keystate == 0:
                ungrab()


                
                commandmode = False
'''
                
ui.close()
