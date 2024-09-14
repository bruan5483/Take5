from pynput.mouse import Controller, Listener
from time import sleep
mouse = Controller()
prev = mouse.position

mouse.position = (0, 0)

def on_move(x, y):
    print(mouse.position)
    mouse.position = (0, 0)


#     global prev

#     mouse.position = (0, 0)

#     # cur = mouse.position
#     # dx = x - prev[0]
#     # dy = y - prev[1]
#     # mouse.position = (x - 2*dx, y - 2*dy)
#     # prev = (x, y)
#     # sleep(0)

def on_click(x, y, button, pressed):
    mouse.move(10, 10)
    
def on_scroll(x, y, dx, dy):
    pass

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=True) as listener:
    listener.join()
