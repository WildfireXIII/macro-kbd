import pyautogui as gui
import evdev
import subprocess


device = evdev.InputDevice('/dev/input/event0')
print(device)

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        #print(categorize(event))
        keyevent = evdev.KeyEvent(event)
        print(keyevent.keycode, keyevent.keystate)

        if keyevent.keycode == 'KEY_A' and keyevent.keystate == 1:
            subprocess.Popen(['python', '/home/dwl/lab/MacroKbd/actuators.py'])


        #if (evdev.ecodes.
