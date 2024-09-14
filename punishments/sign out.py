import platform
import ctypes
import pyautogui

if platform.system() == "Windows":
    ctypes.windll.user32.LockWorkStation()
else:
    pyautogui.keyDown("cmd")
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("q")