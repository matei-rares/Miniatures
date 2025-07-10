from ctypes import *
import os
import random

all_files=[]
FOLDER_PATH = r"C:\Users\matei\Desktop\----\poze backround si altele\backround"
def list_files(folder_path):
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():
                all_files.append(entry.name)
                #print(entry.name)

list_files(FOLDER_PATH)

current_file=random.choice(all_files)
print(current_file)

image_path = FOLDER_PATH + "\\" + current_file

"""SPI_SETDESKWALLPAPER = 20"""
windll.user32.SystemParametersInfoW(20, 0, image_path, 3)