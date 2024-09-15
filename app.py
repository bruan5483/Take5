import pystray
from PIL import Image
from pystray import MenuItem as Item
from threading import Thread
import settings
from main import main

settings.init()

def create_image(state_on):
    """Creates an icon image based on the state."""
    if state_on: return Image.open("iconOn.png")
    else: return Image.open("iconOff.png")

def toggle_state(icon, item):
    """Toggles the state and updates the tray icon."""
    settings.state = not settings.state

    if settings.state: 
        print("Enabled.")
        t = Thread(target=main)
        t.start()
    else: 
        print("Disabled.")

    icon.icon = create_image(settings.state)

def setup(icon):
    """Initial setup of the tray icon, no menu."""
    icon.icon = create_image(settings.state)
    icon.visible = True

menu = pystray.Menu(
    Item("Toggle State", toggle_state, default=True) 
)

icon = pystray.Icon("VZN", icon=create_image(settings.state), menu=menu)
icon.run(setup=setup)
