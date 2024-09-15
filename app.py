import pystray
from PIL import Image
from time import sleep
from pystray import MenuItem as Item
from threading import Thread
# from main import main
import subprocess

with open("settings.txt", "w") as f:
    f.write("stop")

sleep(0.1)
state = False

def run():
    subprocess.run(["python3", "main.py"])

def create_image(state_on):
    """Creates an icon image based on the state."""
    if state_on: return Image.open("iconOn.png")
    else: return Image.open("iconOff.png")

def toggle_state(icon, item):
    global state
    """Toggles the state and updates the tray icon."""
    with open("settings.txt", "r+") as f:
        if not state:
            f.write('')
            print("Enabled.")
            t = Thread(target=run)
            t.start()
            icon.icon = create_image(True)
        else:
            f.write("stop")
            print("Disabled.")
            icon.icon = create_image(False)
    state = not state

def setup(icon):
    """Initial setup of the tray icon, no menu."""
    icon.icon = create_image(state)
    icon.visible = True

menu = pystray.Menu(
    Item("Toggle State", toggle_state, default=True) 
)

icon = pystray.Icon("Take5", icon=create_image(state), menu=menu)
icon.run(setup=setup)
