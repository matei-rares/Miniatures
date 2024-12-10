# Import required modules
import ctypes
from datetime import datetime

import pyautogui
import time
import keyboard  # Library to detect key presses
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002) #this will prevent the screen saver or sleep.

## your code and operations


# FAILSAFE to FALSE feature is enabled by default
# so that you can easily stop execution of
# your pyautogui program by manually moving the
# mouse to the upper left corner of the screen.
# Once the mouse is in this location,
# pyautogui will throw an exception and exit.
pyautogui.FAILSAFE = False
class BreakIt(Exception): pass
# Infinite loop that will run until a specific key is pressed

try:
    while True:

        for i in range(0, 50):
            pyautogui.moveTo(i * 5, i * 6)

            if keyboard.is_pressed("esc") or keyboard.is_pressed("enter") or keyboard.is_pressed("space"):
                print("Exit key pressed. Exiting...")
        
                raise BreakIt
        print(datetime.now())
        time.sleep(2)
except BreakIt:
    pass


ctypes.windll.kernel32.SetThreadExecutionState(0x80000000) #set