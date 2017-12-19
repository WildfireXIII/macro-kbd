import pyautogui as gui


import evdev


device = evdev.InputDevice('/dev/input/event0')
print(device)

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        #print(categorize(event))
        keyevent = evdev.KeyEvent(event)
        print(keyevent.keycode, keyevent.keystate)


        #if (evdev.ecodes.
