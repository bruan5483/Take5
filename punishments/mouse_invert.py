# inverts perfectly but can't click/scroll

from pynput.mouse import Controller, Listener, Button
import mouse
from time import sleep, perf_counter as pf
m = Controller()
prev = m.position

TIME_LIMIT = 5

flag = True

def on_move(x, y):
    global prev
    new = ((prev[0] - x) * 2, (prev[1] - y) * 2)
    sleep(0)
    mouse.move(*new, absolute=False)
    prev = m.position 

def on_click(x, y, button, pressed):
    return flag
    
def on_scroll(x, y, dx, dy):
    pass

start = pf()

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=True) as listener:
    while flag: 
        if pf() - start > TIME_LIMIT:
            flag = False
            mouse.click()
        sleep(0.1)
            
    listener.join()