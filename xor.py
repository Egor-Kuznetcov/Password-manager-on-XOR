from os import urandom


def gen_random(length: int):
    random = []
    for _ in range(length):
        random.append(int.from_bytes(urandom(length), byteorder='big'))
    return random


def encrypt(text: str, key: list):
    with open('alphabet', 'r') as file:
        alph = file.read().split(", ")
        res = []
        for i in range(len(text)):
            res.append((alph.index(text[i]) + key[i]) % len(alph))
        return res


def decrypt(text_en: list, key: list):
    with open('alphabet', 'r') as file:
        alph = file.read().split(", ")
        text = ""
        for i in range(len(text_en)):
            text += alph[(text_en[i] - key[i]) % len(alph)]
        return text


def random_to_key(random: list, master: str, module: int):
    if len(random) > len(master):
        n = (len(random)//len(master))
        master = master*n + master[:(len(random)-len(master)*n)]
    key = []
    for i in range(len(random)):
        key.append(random[i]*ord(master[i]) % module)
    return key
