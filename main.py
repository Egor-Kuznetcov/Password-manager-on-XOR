import re
from xor import *
from TCATO import *
from hashlib import sha256
from os import urandom
import keyboard
import gc


def save(password):
    module = int.from_bytes(urandom(8), byteorder='big')
    random = gen_random(len(password))
    key = random_to_key(random, master_password, module)
    password_en = encrypt(password, key)
    with open("C://PasswordManager/randoms.txt", "a") as file:
        file.write(str(random) + "\n")
    with open("D://passwords.txt", "a") as file:
        file.write(str(password_en) + " " + str(module) + "\n")
    del key
    del module


def read_passwords():
    passwords = []
    with open("C://PasswordManager/randoms.txt", "r") as file:
        randoms = file.readlines()
    with open("D://passwords.txt", "r") as file:
        strings = file.readlines()
    for i in range(len(randoms)):
        random = list(map(int, randoms[i].replace("[", "").replace("]", "").replace("\n", "").split(", ")))
        password, module = strings[i].split("] ")
        password = password.replace("[", "").split(",")
        password = list(map(int, password))
        module = module.replace("\n", "")
        password_dec = decrypt(password, random_to_key(random, master_password, int(module)))
        passwords.append(password_dec)
        del password_dec
        del module

    return passwords


print("Welcome to Password manager on XOR!\n")

try:
    master_password = ""

    file = open("D://user.txt", "a")
    file.close()
    file = open("D://user.txt", "r+")
    user = file.readline()
    if user == "":
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
        file.write(sha.hexdigest())
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
    file.close()

    user_choice = ""

    while user_choice != "exit":
        user_choice = input(">>")
        if user_choice == "help":
            print("save [password] - saves the password\n"
                  "delete [index] - delete password by index\n"
                  "edit [index] - edit password by index\n"
                  "list - shows all passwords\n"
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
            with open("D://passwords.txt", "r") as file:
                strings = file.readlines()
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
                file2 = open("D://passwords.txt", "w")
                for q in passwords:
                    module = int.from_bytes(urandom(4), byteorder='big')
                    random = gen_random(len(q))
                    key = random_to_key(random, master_password, module)
                    password_en = encrypt(q, key)
                    file1.write(str(random) + "\n")
                    file2.write(str(password_en) + " " + str(module) + "\n")
                    del module
                file1.close()
                file2.close()
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
                file2 = open("D://passwords.txt", "w")
                for q in passwords:
                    module = int.from_bytes(urandom(4), byteorder='big')
                    random = gen_random(len(q))
                    key = random_to_key(random, master_password, module)
                    password_en = encrypt(q, key)
                    file1.write(str(random) + "\n")
                    file2.write(str(password_en) + " " + str(module) + "\n")
                    del module
                file1.close()
                file2.close()
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
                file2 = open("D://passwords.txt", "w")
                for q in passwords:
                    module = int.from_bytes(urandom(4), byteorder='big')
                    random = gen_random(len(q))
                    key = random_to_key(random, master_password, module)
                    password_en = encrypt(q, key)
                    file1.write(str(random) + "\n")
                    file2.write(str(password_en) + " " + str(module) + "\n")
                    del module
                file1.close()
                file2.close()
                del q
                del passwords
                del master_password
                gc.collect()
                break
            except:
                print("Error")
        else:
            print("Unknown command, use help to show the list of command.")
except:
    print("Error")
    time.sleep(2)
