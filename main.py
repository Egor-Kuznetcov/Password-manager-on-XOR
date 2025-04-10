import os
import re
from xor import *
from TCATO import *
from hashlib import sha256
import keyboard
import gc


def save(password):
    module = gen_random(1)[0] * gen_random(1)[0]
    random = gen_random(len(password))
    key = random_to_key(random, master_password, module)
    password_en = encrypt(password, key)
    with open("C://PasswordManager/randoms.txt", "a") as file:
        file.write(str(random) + "\n")
    string = str(password_en) + " " + str(module) + "\n"
    ser.write(("1 " + string).encode('utf-8'))
    ser.readline()
    del key
    del module
    del string


def read_passwords():
    passwords = []
    with open("C://PasswordManager/randoms.txt", "r") as file:
        randoms = file.readlines()
    ser.write(b'3')
    string = []
    response = b''
    while b'-'not in response:
        response = ser.readline()
        if b'-' not in response:
            string.append(response.decode('utf-8').replace("\n", "").replace("\r", ""))
    for i in range(len(randoms)):
        random = list(map(int, randoms[i].replace("[", "").replace("]", "").replace("\n", "").split(", ")))
        password, module = string[i].split("] ")
        password = password.replace("[", "").split(",")
        password = list(map(int, password))
        module = module.replace("\n", "")
        password_dec = decrypt(password, random_to_key(random, master_password, int(module)))
        passwords.append(password_dec)
        del password_dec
        del module
    del string

    return passwords


print("Welcome to Password manager on XOR!\n")

try:
    master_password = ""

    ser.write(b'4')
    user = ser.readline().decode('utf-8').replace("\r\n", "")
    if ('a' not in user) and ('7' not in user) and ('0' not in user):
        print("Please create a master-password")
        master_password = ""
        while True:
            master_password = input(">>")
            if len(master_password) < 8 or re.search('[~!?@#$%^&*_\-+()\[\]{}<>/\\\|"\'.,:;]', master_password) is None\
                    or re.search('[0-9]', master_password) is None or re.search('[A-Z]', master_password) is None:
                print("The master password must be at least 8 characters long and contain numbers, "
                      "capital letters and special characters.")
            else:
                break
        sha = sha256()
        sha.update(master_password.encode('utf-8'))
        ser.write(('2 ' + str(sha.hexdigest())).encode('utf-8'))
    else:
        print("Please enter master-password")
        while True:
            master_password = input(">>")
            sha = sha256()
            sha.update(master_password.encode('utf-8'))
            if sha.hexdigest() != user:
                print("Wrong master-password")
            else:
                break

    user_choice = ""

    while user_choice != "exit":
        user_choice = input(">>")
        if user_choice == "help":
            print("save [password] - saves the password\n"
                  "delete [index] - delete password by index\n"
                  "edit [index] - edit password by index\n"
                  "list - shows all passwords\n"
                  "move - copies randoms.txt to external device for transfer\n"
                  "restore - transfers data from an external device to randoms.txt\n"
                  "exit - exit from password manager\n"
                  "select [index] - select password by index\n"
                  "Press 'p' to auto-type selected password")
        elif "save " in user_choice:
            try:
                password = user_choice.split(" ")[1]
                save(password)
                del password
                gc.collect()
            except:
                print("Error")
        elif user_choice == "list":
            with open("C://PasswordManager/randoms.txt", "r") as file:
                randoms = file.readlines()
            ser.write(b'3')
            strings = []
            response = b''
            while b'-' not in response:
                response = ser.readline()
                if b'-' not in response:
                    strings.append(response.decode('utf-8').replace("\r\n", ""))
            count = 0
            for i in range(len(randoms)):
                count += 1
                random = list(map(int, randoms[i].replace("[", "").replace("]", "").replace("\n", "").split(", ")))
                password, module = strings[i].split("] ")
                password = password.replace("[", "").split(",")
                password = list(map(int, password))
                module = module.replace("\n", "")
                password_dec = decrypt(password, random_to_key(random, master_password, int(module)))
                print(str(count) + ") " + password_dec)
                del password
                del module
                del password_dec
            del strings
            del randoms
            gc.collect()
        elif "delete " in user_choice:
            try:
                index = int(user_choice.split(" ")[1])
                passwords = read_passwords()
                passwords.pop(index-1)
                file1 = open("C://PasswordManager/randoms.txt", "w")
                ser.write(b'7')
                ser.readline()
                for q in passwords:
                    module = gen_random(1)[0] * gen_random(1)[0]
                    random = gen_random(len(q))
                    key = random_to_key(random, master_password, module)
                    password_en = encrypt(q, key)
                    file1.write(str(random) + "\n")
                    ser.write(("1 " + str(password_en) + " " + str(module) + "\n").encode('utf-8'))
                    ser.readline()
                    del module
                file1.close()
                del q
                del passwords
                gc.collect()
                print(f"Password {index} deleted")
            except:
                print("Error")
        elif "edit " in user_choice:
            try:
                index = int(user_choice.split(" ")[1])
                passwords = read_passwords()
                print("Enter edited password")
                passwords[index - 1] = input(">>")
                file1 = open("C://PasswordManager/randoms.txt", "w")
                ser.write(b'7')
                ser.readline()
                for q in passwords:
                    module = gen_random(1)[0] * gen_random(1)[0]
                    random = gen_random(len(q))
                    key = random_to_key(random, master_password, module)
                    password_en = encrypt(q, key)
                    file1.write(str(random) + "\n")
                    ser.write(("1 " + str(password_en) + " " + str(module) + "\n").encode('utf-8'))
                    ser.readline()
                    del module
                file1.close()
                del q
                del passwords
                gc.collect()
                print(f"Password {index} edited")
            except:
                print("Error")
        elif "select " in user_choice:
            try:
                index = int(user_choice.split(" ")[1])
                passwords = read_passwords()
                selected_pass = passwords[index-1]
                print(f"Password {index} selected")
                keyboard.wait("p")
                keyboard.press_and_release("backspace")
                time.sleep(0.007)
                two_channel_obfuscation(selected_pass)
                del passwords
                del selected_pass
                gc.collect()
            except:
                print("Error")
        elif user_choice == "exit":
            try:
                passwords = read_passwords()
                file1 = open("C://PasswordManager/randoms.txt", "w")
                ser.write(b'7')
                ser.readline()
                for q in passwords:
                    module = gen_random(1)[0] * gen_random(1)[0]
                    random = gen_random(len(q))
                    key = random_to_key(random, master_password, module)
                    password_en = encrypt(q, key)
                    file1.write(str(random) + "\n")
                    ser.write(("1 " + str(password_en) + " " + str(module) + "\n").encode('utf-8'))
                    ser.readline()
                    del module
                file1.close()
                del q
                del passwords
                del master_password
                gc.collect()
                break
            except:
                print("Error")
        elif user_choice == "move":
            try:
                with open("C://PasswordManager/randoms.txt", "r") as file:
                    randoms = file.readlines()
                os.remove("C://PasswordManager/randoms.txt")
                for line in randoms:
                    ser.write(("5 " + line).encode('utf-8'))
                    ser.readline()
            except:
                print("Error")
        elif user_choice == "restore":
            try:
                response = b''
                ser.write(b'6')
                randoms = []
                while b'-' not in response:
                    response = ser.readline()
                    if b'-' not in response:
                        randoms.append(response.decode('utf-8').replace("\r\n", ""))
                with open("C://PasswordManager/randoms.txt", "w") as file:
                    for random in randoms:
                        file.write(random)
            except:
                print("Error")
        else:
            print("Unknown command, use help to show the list of command.")
except:
    print("Error")
    time.sleep(2)
