"""
This script makes no perminant changes to the system.

- Set the mouse speed
  - Via the registerty (so it does not reset)
  - In memory (to take effect immidiatly)
- Change the background image (uses the windows API)
- Enables num-lock
- Dissables light mode
- Modifies taskbar
  - Dissables 'task view'
  - Dissables search bar
  - Moves to the left
"""

import winreg
from winreg import HKEY_CURRENT_USER, REG_SZ, REG_DWORD
import ctypes
import win32con
import os
import subprocess
import traceback

# TODO:
# - figure out how to change the regestry keys to set default programs for most things
#     to notepad++
#   - default browser to chrome
#     - and for PDF's
# - extract the chrome profile and copy it back across to attempt to preserve logins
#   - And change the stupid search engine
# - Fix powertoys


MOUSESPEED = 20
BACKGROUNDPATH = rb"\\userfs\tqb510\w2k\Desktop\background.jpg"
POWERTOYS = r"\\userfs\tqb510\w2k\Desktop\powertoysinstall.exe"

REGCHANGES = [
    (HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseSensitivity",
     REG_SZ, str(MOUSESPEED), "change|d the mouse speed"),
    (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme",
     REG_DWORD, 0, "disable|d system light mode"),
    (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme",
     REG_DWORD, 0, "disable|d light mode"),
    (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowTaskViewButton",
     REG_DWORD, 0, "disable|d taskbar task view"),
    (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Search", "SearchboxTaskbarMode",
     REG_DWORD, 0, "disable|d taskbar search box"),
    (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarAl",
     REG_DWORD, 0, "change|d the taskbar alignment"),

]


def set_reg_entry(hkey, reg_path, name, data_type, value, description):
    print(f"[         ] Attempting to {description.replace('|d', '')}...")

    try:
        winreg.CreateKey(hkey, reg_path)

        with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, name, 0, data_type, value)

    except WindowsError as e:
        print(f"[ \033[31mFAIL\033[0m    ] Unable to {description.replace('|d', '')}, {e}. Printing traceback\n")
        traceback.print_exc()

    else:
        print(f"[ \033[32mSUCCESS\033[0m ] Set {description.replace('|', '')}")


def set_mouse_speed(speed):
    res = ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETMOUSESPEED, 0, speed, 0x01 | 0x02)

    if res == 0:
        print("[ \033[31mFAIL\033[0m    ] Did not set current mouse speed")
    elif res == 1:
        print("[ \033[32mSUCCESS\033[0m ] Set mouse current speed")
    else:
        raise SystemError(f"Got unknown response code from windll, current mouse speed, result {res}")


def set_background_image(path):
    path = b''.join(c.to_bytes(2, 'little') for c in path)
    buffer = ctypes.create_string_buffer(path, 255 * 4)
    res = ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 255, buffer, 0x01 | 0x02)

    if res == 0:
        print("[ \033[31mFAIL\033[0m    ] Did not set background image")
    elif res == 1:
        print("[ \033[32mSUCCESS\033[0m ] Set background image")
    else:
        raise SystemError(f"Got unknown response code from windll, wallpaper, response {res}")


def set_numlock():
    cur = ctypes.windll.user32.GetKeyState(win32con.VK_NUMLOCK)

    if cur == 1:
        print("[ SKIP    ] Numlock already on")
    elif cur == 0:
        ctypes.windll.user32.keybd_event(win32con.VK_NUMLOCK, 0x3a, 0x1, 0)
        ctypes.windll.user32.keybd_event(win32con.VK_NUMLOCK, 0x3a, 0x3, 0)
        print("[ \033[32mSUCCESS\033[0m ] Set noblock")
    else:
        raise SystemError(f"Got unknown response code from windll, numlock, result {res}")

# Set all the reg entries
for reg in REGCHANGES:
    set_reg_entry(*reg)

# Set mouse speed
set_mouse_speed(MOUSESPEED)

# Set background image
set_background_image(BACKGROUNDPATH)

# Turn on num lock
set_numlock()


# Call powertoys install
# res = subprocess.call([POWERTOYS, "/install", "/passive"])

# if res == 0:
#     print("[ SUCCESS ] PowerToys installed, exit 0")
# else:
#     raise SystemError(f"PowerToys installer exited non 0, exit {res}")
