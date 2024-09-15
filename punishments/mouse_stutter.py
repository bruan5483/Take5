import pyautogui
import time

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = pyautogui.position()

while True:
    current_x, current_y = pyautogui.position()
    dx = current_x - prev_x
    dy = current_y - prev_y
    inverted_x = prev_x - dx*3
    inverted_y = prev_y - dy*3

    pyautogui.moveTo(inverted_x, inverted_y)
    prev_x, prev_y = pyautogui.position()

    time.sleep(0.01)