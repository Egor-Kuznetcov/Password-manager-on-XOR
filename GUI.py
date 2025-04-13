import sys
import time
import keyboard
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from TCATO import two_channel_obfuscation
import re
from hashlib import sha256
from xor import *
import gc
import os
from kivy.config import Config

Config.set('graphics', 'resizable', '0');
Config.set('graphics', 'width', '600');
Config.set('graphics', 'height', '800');
Config.write();

passwords = []


class RestoreScreen(Screen):
    def __init__(self, **kwargs):
        super(RestoreScreen, self).__init__(**kwargs)
        flt_layout = FloatLayout()
        img = Image(source='Background.png')
        flt_layout.add_widget(img)
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        anchor.add_widget(Button(text='Restore', font_size=60, on_press=self.restore,
                                 background_normal="", background_color=[0.27, 0.41, 0.93, 1],
                                 size_hint=[None, None], size=[500, 400]))
        flt_layout.add_widget(anchor)
        self.add_widget(flt_layout)

    def restore(self, instance):
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
        sm.current = 'login'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        ser.write(b'4')
        self.password = ser.readline().decode('utf-8').replace('\r\n', "")
        if ('a' not in self.password) and ('7' not in self.password) and ('0' not in self.password):
            sm.add_widget(RegistrationScreen(name='registration'))
            sm.current = 'registration'
        self.label = Label(text="Please enter password", size_hint=[None, None],
                           size=[200, 75], pos=[200, 575], font_size=35)
        self.text = TextInput(password=True, multiline=False, allow_copy=False,
                              size_hint=[None, None], size=[500, 35], pos=[50, 400])
        self.button = Button(text="Enter", background_normal="", background_color=[0.27, 0.41, 0.93, 1],
                             size_hint=[None, None], size=[300, 150], font_size=25, pos=[150, 125])
        self.button.bind(on_press=self.check)
        self.layout = FloatLayout()
        img = Image(source='Background.png')
        self.layout.add_widget(img)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)
        self.master_password = ""

    def check(self, instance):
        self.master_password = self.text.text
        sha = sha256()
        sha.update(self.master_password.encode('utf-8'))
        if sha.hexdigest() != self.password:
            self.label.text = "Wrong password!"
            self.text.text = ""
        else:
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'main'


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        self.label = Label(text="Please create master-password", size_hint=[None, None],
                           size=[200, 75], pos=[200, 575], font_size=35)
        self.text = TextInput(password=True, multiline=False, allow_copy=False,
                              size_hint=[None, None], size=[500, 35], pos=[50, 400])
        self.button = Button(text="Create", background_normal="", background_color=[0.27, 0.41, 0.93, 1],
                             size_hint=[None, None], size=[300, 150], font_size=25, pos=[150, 125])
        self.button.bind(on_press=self.check)
        self.layout = FloatLayout()
        img = Image(source="Background.png")
        self.layout.add_widget(img)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)
        self.master_password = ""

    def check(self, instance):
        self.master_password = self.text.text
        if len(self.master_password) < 8 or re.search('[~!?@#$%^&*_\-+()\[\]{}<>/\\\|"\'.,:;]',
                                                      self.master_password) is None \
                or re.search('[0-9]', self.master_password) is None or re.search('[A-Z]', self.master_password) is None:
            self.label.text = ("The master password must be at least 8 characters long and contain numbers, "
                               "capital letters and special characters.")
        else:
            sha = sha256()
            sha.update(self.master_password.encode('utf-8'))
            ser.write(('2 ' + str(sha.hexdigest())).encode('utf-8'))
            sm.current = 'login'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint=[None, None], size=[600, 800])
        img = Image(source="Background.png")
        flt_layout = FloatLayout()
        flt_layout.add_widget(img)
        flt_layout.add_widget(self.layout)
        self.save_layout = BoxLayout(orientation='horizontal', size_hint=[None, None])
        self.big_save_layout = BoxLayout(size_hint=[None, None], size=[600, 80])
        save_anchor = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=[None, None], size=[600, 80])
        self.big_save_layout.add_widget(save_anchor)
        self.pas = TextInput(multiline=False, allow_copy=False, size_hint=[None, None],
                             size=[400, 35])
        anchor = AnchorLayout(anchor_x='left', anchor_y='center')
        anchor.add_widget(self.pas)
        self.save_layout.add_widget(anchor)
        self.save_layout.add_widget(Button(text="Save", on_press=self.add,
                                           background_normal="", background_color=[0.27, 0.41, 0.93, 1],
                                           size_hint=[None, None], size=[100, 75]))
        self.save_layout.add_widget(Button(text='Move', color=[0.09, 0.15, 0.39, 1], on_press=self.move,
                                           background_normal="", background_color=[0.63, 0.99, 1, 1],
                                           size_hint=[None, None], size=[100, 75]))
        self.save_layout.size = [600, 75]
        save_anchor.add_widget(self.save_layout)
        self.layout.add_widget(self.big_save_layout)
        self.add_widget(flt_layout)
        self.scroll = ScrollView(scroll_type=['bars', 'content'], scroll_distance=35, scroll_y=1, do_scroll_x=False,
                                 do_scroll_y=True, always_overscroll=True,
                                 bar_width=5, bar_pos_y='right', size_hint=[1, None], size=[600, 725])
        self.scroll_layout = GridLayout(cols=1, spacing=5, size_hint=[None, None], size=[600, 0])
        self.scroll.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll)
        global passwords
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
            password_dec = decrypt(password, random_to_key(random, loginscreen.master_password, int(module)))
            self.scroll_layout.add_widget(self.create_new_block(password_dec))
            passwords.append(password_dec)
            del module
            del password_dec
        ser.write(b'7')
        ser.readline()
        del strings
        del randoms
        gc.collect()

    def add(self, instance):
        global passwords
        passwords.append(self.pas.text)
        self.scroll_layout.add_widget(self.create_new_block(text=self.pas.text))

    def create_new_block(self, text):
        self.pas.text = ""
        box = BoxLayout(orientation='horizontal', size_hint=[None, None], size=[595, 35])
        label = Label(text=text, size_hint=[None, None], size=[400, 35])
        box.add_widget(label)
        box.add_widget(Button(text="Select", color=[0.09, 0.15, 0.39, 1],
                              background_normal="", background_color=[0.92, 0.77, 0.54, 1],
                              size_hint=[None, None], size=[100, 35],
                              on_release=lambda instance: (keyboard.wait('p'),
                                                           keyboard.press_and_release('backspace'),
                                                           time.sleep(0.007),
                                                           two_channel_obfuscation(label.text))))
        box.add_widget(Button(text='Delete',
                              on_press=lambda instance: self.delete(label_text=label.text),
                              on_release=lambda x: self.delete_widget(layout=box),
                              size_hint=[None, None], size=[90, 35],
                              background_normal="", background_color=[0.8, 0.04, 0.04, 1]))
        self.scroll_layout.size = [600, self.scroll_layout.size[1]+40]
        return box

    def delete(self, label_text):
        global passwords
        passwords.remove(label_text)

    def delete_widget(self, layout):
        layout.parent.remove_widget(layout)
        self.scroll_layout.size=[600, self.scroll_layout.size[1]-40]

    def move(self, instance):
        global passwords
        file1 = open("C://PasswordManager/randoms.txt", "w")
        ser.write(b'7')
        ser.readline()
        for q in passwords:
            module = gen_random(1)[0] * gen_random(1)[0]
            random = gen_random(len(q))
            key = random_to_key(random, loginscreen.master_password, module)
            password_en = encrypt(q, key)
            file1.write(str(random) + "\n")
            ser.write(("1 " + str(password_en) + " " + str(module) + "\n").encode('utf-8'))
            ser.readline()
            del module
        file1.close()
        del q
        del loginscreen.master_password
        gc.collect()
        with open("C://PasswordManager/randoms.txt", "r") as file:
            randoms = file.readlines()
        os.remove("C://PasswordManager/randoms.txt")
        for line in randoms:
            ser.write(("5 " + line).encode('utf-8'))
            ser.readline()
        ser.close()
        Password_Manager_on_XORApp().stop_now()


sm = ScreenManager()
loginscreen = LoginScreen(name='login')
sm.add_widget(loginscreen)


class Password_Manager_on_XORApp(App):
    def build(self):
        try:
            open("C://PasswordManager/randoms.txt", 'r')
            sm.current = 'login'
        except:
            sm.add_widget(RestoreScreen(name='restore'))
            sm.current = 'restore'
        return sm

    def on_stop(self):
        global passwords
        file1 = open("C://PasswordManager/randoms.txt", "w")
        for q in passwords:
            module = gen_random(1)[0] * gen_random(1)[0]
            random = gen_random(len(q))
            key = random_to_key(random, loginscreen.master_password, module)
            password_en = encrypt(q, key)
            file1.write(str(random) + "\n")
            ser.write(("1 " + str(password_en) + " " + str(module) + "\n").encode('utf-8'))
            ser.readline()
            del module
        file1.close()
        del q
        del loginscreen.master_password
        gc.collect()
        ser.close()

    def stop_now(self):
        sys.exit()


Password_Manager_on_XORApp().run()
