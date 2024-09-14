# inverts perfectly but can't click/scroll

from pynput.mouse import Controller, Listener, Button
import mouse
from time import sleep
m = Controller()
prev = m.position


def on_move(x, y):
    global prev

    new = ((prev[0] - x) * 2, (prev[1] - y) * 2)
    sleep(0)
    mouse.move(*new, absolute=False)
    prev = m.position 

def on_click(x, y, button, pressed):
    pass

def on_scroll(x, y, dx, dy):
    pass

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=True) as listener:
    listener.join()