import ctypes
from datetime import datetime
import pyautogui
import time
import keyboard  
import pygetwindow as gw


ctypes.windll.kernel32.SetThreadExecutionState(0x80000002) # start preventing sleep
pyautogui.FAILSAFE = False
class BreakIt(Exception): pass


#WORKS: set volume of audio device
def set_device_volume_mute_state(level, mute = 1):  # level: 0.0 to 1.0 , mute: 0 or 1
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(mute, None)
    volume.SetMasterVolumeLevelScalar(level, None)
    print(f"Volume set to {int(level * 100)}% and mute state set to {'Muted' if mute == 1 else 'Unmuted'}.")
#set_system_volume(0.5)  # 50%



def set_default_audio_device(device_name):
    import subprocess
    import os
    exe_path = os.path.join(os.path.dirname(__file__), "SoundVolumeView.exe")
    subprocess.run([ exe_path,"/SetDefault", device_name, "1"], check=True)

def switch_to_tab():
    teams_window = None
    for window in gw.getAllWindows():
        if "Microsoft Teams" in window.title: 
            teams_window = window
            break 

    if teams_window:
        teams_window.activate()
        return teams_window.left, teams_window.top
    else:
        #launch teams
        print("Teams window not found")

#TODO download https://www.nirsoft.net/utils/soundvolumeview-x64.zip and unzip it in the same folder as this script
speakers = "{0.0.0.00000000}.{21615d7d-381e-41a8-b146-74bd1b3a0977}" #speakers
headset = "{0.0.0.00000000}.{defec8ec-6afe-4c01-85bd-61d0c7950da5}" #jabra headset
try:
    x,y=switch_to_tab()
    #x,y=0,0
    set_default_audio_device(speakers) #speakers
    set_device_volume_mute_state(level = 1,mute = 0)  # Set volume to 100%
    while True:

        for i in range(0, 50):
            pyautogui.moveTo(x+i * 5,y+ i * 6)

            if keyboard.is_pressed("esc") or keyboard.is_pressed("enter") or keyboard.is_pressed("space"):
                print("Exit key pressed. Exiting...")
        
                raise BreakIt
        print(datetime.now()) 
        time.sleep(2)
except BreakIt:
    set_device_volume_mute_state(level = 1,mute = 1)
    set_default_audio_device(headset) #jabra
    set_device_volume_mute_state(level = 0.7,mute = 0)
    pass


ctypes.windll.kernel32.SetThreadExecutionState(0x80000000) #end 