import platform
import ctypes
import pyautogui

if platform.system() == "Windows":
    ctypes.windll.user32.LockWorkStation()
else:
    pyautogui.keyDown("command")
    pyautogui.keyDown("ctrl")
    pyautogui.press("q")