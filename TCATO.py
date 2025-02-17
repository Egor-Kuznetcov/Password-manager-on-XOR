import time

import keyboard
from hashlib import sha256
import pyperclip
import win32gui
from win32api import PostMessage, GetKeyboardLayoutName


def two_channel_obfuscation(string: str):
    spec_sym = "{}()+^%"
    string_res = []
    part = ""
    hash_obj = sha256()
    window_handle = win32gui.GetForegroundWindow()
    flag = False
    clipboard_part = ""

    for char in range(len(string)):
        if char != len(string) - 1:
            if string[char] not in spec_sym:
                part += string[char]
            else:
                if part != "":
                    string_res.append(part)
                string_res.append(string[char])
                part = ""
        elif (char == len(string) - 1) and string[char] in spec_sym:
            string_res.append(part)
            string_res.append(string[char])
            part = ""
        else:
            string_res.append(part + string[char])
            part = ""

    if GetKeyboardLayoutName() != "00000409":
        PostMessage(window_handle, 0x0050, 0, 0x4090409)
    else:
        flag = False

    for i in string_res:
        if len(i) == 1 and i in spec_sym:
            keyboard.write(i)
        else:
            hash_obj.update(i.encode('utf-8'))
            print_part = list(i)
            big_num = str(int(hash_obj.hexdigest(), 16))
            syms = []
            for num in range(len(i) // 2):
                ind = int(big_num[num]) % len(i)
                syms.append(ind)
            syms.sort()
            syms = set(syms)

            for sym in syms:
                clipboard_part += i[sym]
                print_part.pop(sym)
                print_part.insert(sym, "+")

            pyperclip.copy(clipboard_part)
            keyboard.press_and_release("ctrl + v")
            time.sleep(0.007)

            for m in range(len(clipboard_part)):
                keyboard.press_and_release("left")
                time.sleep(0.007)

            for q in print_part:
                if q == "+":
                    keyboard.press_and_release("right")
                    time.sleep(0.007)
                else:
                    keyboard.write(q)
        clipboard_part = ""

    if flag:
        PostMessage(window_handle, 0x0050, 0, 0x4190419)
