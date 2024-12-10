from ctypes import windll

"""
it's just an example of how ctypes can call Windows API functions located in user32.dll
here is a message box with documentation from https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
here you can find more functions: https://learn.microsoft.com/en-us/windows/win32/api/winuser/
"""

user32 = windll.user32
user32.MessageBoxW(0, "Hello, ctypes!", "Example", 2)

screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
print(f"Screen Resolution: {screen_width}x{screen_height}")
