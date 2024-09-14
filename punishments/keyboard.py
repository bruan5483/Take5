# messes up your keyboard

from pynput.keyboard import Key, Controller, Listener

k = Controller()

keys = list("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ[]\;',./{}|:\"<>?_+!@#$%^&*()")

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
        # Stop listener
        return False

# Start listening to keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
