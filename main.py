# import winreg
# from winreg import HKEY_CURRENT_USER, REG_SZ, REG_DWORD
# import ctypes
# import win32con
import os
import sys
import traceback
# import subprocess
# import traceback
from pprint import pprint
import importlib
import requests


COMMIT_URL = "https://api.github.com/repos/actorpus/unidesktopsetup/commits?per_page=1"
CONTENT_URL = "https://raw.githubusercontent.com/actorpus/unidesktopsetup/refs/heads/master/main.py"


print("[ UPDATE  ] Getting remote version.")

commit = requests.get(COMMIT_URL)

assert commit.status_code == 200, f"Got status code {commit.status_code} from remote"

remote_version_sha = commit.json()[0]['sha']

# =================== LINE MODIFIED BY CODE ================= #
#                                                             #
LOCAL_VERSION = '54d7625888f2c64dc12a5668f61a5b12a11348c8'    #
ON_NEW_VERSION = False                                        #
#                                                             #
# =========================================================== #

if not ON_NEW_VERSION:
    if LOCAL_VERSION != remote_version_sha:
        print("[ UPDATE  ] Local version is not up to date, updating.")

        remote = requests.get(CONTENT_URL)

        assert remote.status_code == 200, f"Got status code {remote.status_code} from remote"

        print("[ UPDATE  ] Running new version, Ignore up to date message.")

        file = remote.text

        file = file.replace(
            f"LOCAL_VERSION = '{LOCAL_VERSION}'    #",
            f"LOCAL_VERSION = '{remote_version_sha}'    #"
        )

        # Temporary so self modification doesn't break the script
        virtualized = file.replace(
            f"ON_NEW_VERSION = False                                        #",
            f"ON_NEW_VERSION = True                                         #"
        )

        try:
            exec(virtualized)
        except Exception as e:
            print("[ UPDATE  ] Failed to run new version, printing traceback.")
            traceback.print_exc()
            print("[ UPDATE  ] New version has not been written to disk.")
            sys.exit(1)

        print("[ UPDATE  ] Writing new version to disk.")

        with open(__file__, 'w') as f:
            f.write(file)

        print("[ UPDATE  ] Successfully updated.")

    else:
        print("[ UPDATE  ] Local version is up to date.")

else:
    print("[ \033[0;33mUPDATE\033[0;0m  ] Running virtualized version, disabled update")


print("wooo")

# MOUSESPEED = 20
# BACKGROUNDPATH = rb"\\userfs\tqb510\w2k\Desktop\background.jpg"
# POWERTOYS = r"\\userfs\tqb510\w2k\Desktop\powertoysinstall.exe"
#
# REGCHANGES = [
#     (HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseSensitivity",
#      REG_SZ, str(MOUSESPEED), "change|d the mouse speed"),
#     (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme",
#      REG_DWORD, 0, "disable|d system light mode"),
#     (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme",
#      REG_DWORD, 0, "disable|d light mode"),
#     (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowTaskViewButton",
#      REG_DWORD, 0, "disable|d taskbar task view"),
#     (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Search", "SearchboxTaskbarMode",
#      REG_DWORD, 0, "disable|d taskbar search box"),
#     (HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarAl",
#      REG_DWORD, 0, "change|d the taskbar alignment"),
#
# ]
#
#
# def set_reg_entry(hkey, reg_path, name, data_type, value, description):
#     print(f"[         ] Attempting to {description.replace('|d', '')}...")
#
#     try:
#         winreg.CreateKey(hkey, reg_path)
#
#         with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_WRITE) as key:
#             winreg.SetValueEx(key, name, 0, data_type, value)
#
#     except WindowsError as e:
#         print(f"[ \033[31mFAIL\033[0m    ] Unable to {description.replace('|d', '')}, {e}. Printing traceback\n")
#         traceback.print_exc()
#
#     else:
#         print(f"[ \033[32mSUCCESS\033[0m ] Set {description.replace('|', '')}")
#
#
# def set_mouse_speed(speed):
#     res = ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETMOUSESPEED, 0, speed, 0x01 | 0x02)
#
#     if res == 0:
#         print("[ \033[31mFAIL\033[0m    ] Did not set current mouse speed")
#     elif res == 1:
#         print("[ \033[32mSUCCESS\033[0m ] Set mouse current speed")
#     else:
#         raise SystemError(f"Got unknown response code from windll, current mouse speed, result {res}")
#
#
# def set_background_image(path):
#     path = b''.join(c.to_bytes(2, 'little') for c in path)
#     buffer = ctypes.create_string_buffer(path, 255 * 4)
#     res = ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 255, buffer, 0x01 | 0x02)
#
#     if res == 0:
#         print("[ \033[31mFAIL\033[0m    ] Did not set background image")
#     elif res == 1:
#         print("[ \033[32mSUCCESS\033[0m ] Set background image")
#     else:
#         raise SystemError(f"Got unknown response code from windll, wallpaper, response {res}")
#
#
# def set_numlock():
#     cur = ctypes.windll.user32.GetKeyState(win32con.VK_NUMLOCK)
#
#     if cur == 1:
#         print("[ SKIP    ] Numlock already on")
#     elif cur == 0:
#         ctypes.windll.user32.keybd_event(win32con.VK_NUMLOCK, 0x3a, 0x1, 0)
#         ctypes.windll.user32.keybd_event(win32con.VK_NUMLOCK, 0x3a, 0x3, 0)
#         print("[ \033[32mSUCCESS\033[0m ] Enabled numlock")
#     else:
#         raise SystemError(f"Got unknown response code from windll, numlock")
#
# # Set all the reg entries
# for reg in REGCHANGES:
#     set_reg_entry(*reg)
#
# # Set mouse speed
# set_mouse_speed(MOUSESPEED)
#
# # Set background image
# set_background_image(BACKGROUNDPATH)
#
# # Turn on num lock
# set_numlock()
#
#
# # Call powertoys install
# # res = subprocess.call([POWERTOYS, "/install", "/passive"])
#
# # if res == 0:
# #     print("[ SUCCESS ] PowerToys installed, exit 0")
# # else:
# #     raise SystemError(f"PowerToys installer exited non 0, exit {res}")
