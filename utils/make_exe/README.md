PyInstaller is tested against Windows, macOS, and Linux.
However, it is not a cross-compiler; to make a Windows app
you run PyInstaller on Windows, and to make a Linux app you run it on Linux

https://pyinstaller.org/en/stable/

#Install pyinstaller
pip install pyinstaller

#If you want to create a single executable file
pyinstaller --onefile .\file.py

#If you want to create a folder with the executable file
pyinstaller .\file.py
