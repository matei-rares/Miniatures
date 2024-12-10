import pyautogui
import keyboard

while True:
    x, y = pyautogui.position()
    print(f"Current mouse position: ({x}, {y})")
    if keyboard.is_pressed('esc'):
        print("\nEsc key pressed. Exiting the loop.")
        break