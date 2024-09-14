import mouse
from time import sleep

last_pos = mouse.get_position()

flag = True

def on_move(event):
    global last_pos

    if isinstance(event, mouse._mouse_event.MoveEvent) and flag:
        new_pos = ((last_pos[0] - event.x) * 2, (last_pos[1] - event.y) * 2)
        mouse.move(*new_pos, absolute=False)
        last_pos = mouse.get_position()


mouse.hook(on_move)

sleep(5)
flag = False # off

sleep(5)