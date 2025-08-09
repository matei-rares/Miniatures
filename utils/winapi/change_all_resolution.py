import win32api
import win32con
import pywintypes
from screeninfo import get_monitors


"""
Change resolution for all monitors to 1920x1080 when first called
At the second call, change the resolution to the maximum resolution of the monitor
(i use this script when my potato can't handle a game made in 2025)
"""

monitors = get_monitors()

width = 1920
height = 1080


def set_resolution(device_name, width, height):
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    result = win32api.ChangeDisplaySettingsEx(device_name, devmode)

    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        print(f"Success ({width}x{height})for {device_name}")
    else:
        print(f"Failed for {device_name}, error code: {result}")


def get_current_resolution(device_name):
    devmode = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)
    return devmode.PelsWidth, devmode.PelsHeight

def get_recommended_resolution(device_name):
    i = 0
    max_resolution = (0, 0)

    while True:
        try:
            devmode = win32api.EnumDisplaySettings(device_name, i)
            if (devmode.PelsWidth * devmode.PelsHeight) > (max_resolution[0] * max_resolution[1]):
                max_resolution = (devmode.PelsWidth, devmode.PelsHeight)
            i += 1
        except:
            break

    return max_resolution


for monitor in monitors:
    device = monitor.name
    n_w, n_h = get_recommended_resolution(device)
    c_w, c_h = get_current_resolution(device)

    if c_w == n_w and c_h == n_h:
        set_resolution(device, width, height)
    else:
        set_resolution(device, n_w, n_h)
    #print(f"Recommended resolution for {device}: {n_w}x{n_h}")
