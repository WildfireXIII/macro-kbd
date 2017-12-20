import pyautogui as gui
import evdev
import subprocess
import keyboard

from evdev import UInput, ecodes as e



listenmode = False # caps lock pressed, wait for a for sequence start
commandmode = False







#gui.keyDown('caps')
#gui.keyDown('f')
#gui.keyUp('f')


#gui.hotkey('caps', 'f')


ui = UInput()

device = evdev.InputDevice('/dev/input/event0')
print(device)

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        #print(evdev.categorize(event))
        ke = evdev.KeyEvent(event)
        print(ke.keycode, ke.keystate)

        if not listenmode and not commandmode: # wait for caps lock
            if ke.keycode == 'KEY_CAPSLOCK' and ke.keystate == 1:
                listenmode = True
        elif listenmode: # caps lock is down
            
            # if a is pressed (sequence to enter command mode)
            if ke.keycode == 'KEY_A' and ke.keystate == 1:
                ui.write_event(ke)
                ui.write(e.EV_KEY, e.KEY_CAPSLOCK, 0)
                ui.write(e.EV_KEY, e.KEY_A, 0)
                ui.syn()
                
                commandmode = True
                print("COMMAND MODE")

                try: 
                    device.grab()
                    print("grabbed")
                except: pass
            elif ke.keystate != 2: # ignore held down keys
                listenmode = False
        elif commandmode:
            if ke.keycode == 'KEY_ENTER' and ke.keystate == 0:
                try: 
                    device.ungrab()
                    print("ungrabbed")
                except: pass
                commandmode = False
                ui.write(e.EV_KEY, e.KEY_CAPSLOCK, 1)
                ui.write(e.EV_KEY, e.KEY_CAPSLOCK, 0)
                ui.syn()


                
                #ui.write(e.EV_KEY, e.KEY_F, 0)
                #ui.write_event(ke)
                
                
        

        #if ke.keycode == 'KEY_A' and ke.keystate == 1:
            #subprocess.Popen(['python', '/home/dwl/lab/MacroKbd/actuators.py'])
            #try: device.grab()
            #except: print(" - Failed to grab")

            #ui.write(e.EV_KEY, e.KEY_A, 0)
            #ui.syn()
            
            
        #if ke.keycode == 'KEY_B' and ke.keystate == 0:
            #try: device.ungrab()
            #except: print(" - Failed to grab")


        #if (evdev.ecodes.

ui.close()
