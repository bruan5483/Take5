# messes up your keyboard

from pynput.keyboard import Key, Controller, Listener
from time import sleep, perf_counter as pf

k = Controller()

TIME_LIMIT = 10

keys = list("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ[]\;',./{}|:\"<>?_+!@#$%^&*()")

flag = True

def on_press(key):
    try:
        if key.char in keys:
            k.press(Key.backspace)
            k.release(Key.backspace)
            new = chr(ord(key.char) + 100)
            k.press(new)
            k.release(new)
    except AttributeError:
        pass

def on_release(key):
    if key == Key.esc:
        return False

# Start listening to keyboard events
start = pf()   
with Listener(on_press=on_press, on_release=on_release) as listener:
    while flag: 
        if pf() - start > TIME_LIMIT:
            flag = False
            k.press(Key.esc)
            k.release(Key.esc)
        sleep(0.1)

    listener.join()

