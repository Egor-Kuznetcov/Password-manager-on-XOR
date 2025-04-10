import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
com = ""
flag = False
for port in ports:
    if "USB-SERIAL CH340" in str(port.description):
        com = str(port.device)
        flag = True
if not flag:
    print("External device error")

ser = serial.Serial(com, 9600)

if b"Card Ready" not in ser.readline():
    print("Card error")


def gen_random(length: int):
    random = []
    ser.write(("0 " + str(length)).encode('utf-8'))
    for _ in range(length):
        response = ser.readline().decode('utf-8')
        response = [response[i:i+3] for i in range(0, len(response), 3)]
        num = ""
        for bit in response:
            if bit != max(set(response), key=response.count):
                num += '1'
            else:
                num += '0'
        random.append(int(num, 2))
    return random


def encrypt(text: str, key: list):
    with open('alphabet', 'r') as file:
        alph = file.read().split(", ")
        res = []
        for i in range(len(text)):
            res.append((alph.index(text[i]) + key[i]) % len(alph))
        del text
        del key
        return res


def decrypt(text_en: list, key: list):
    with open('alphabet', 'r') as file:
        alph = file.read().split(", ")
        text = ""
        for i in range(len(text_en)):
            text += alph[(text_en[i] - key[i]) % len(alph)]
        del key
        return text


def random_to_key(random: list, master: str, module: int):
    if len(random) > len(master):
        n = (len(random)//len(master))
        master = master*n + master[:(len(random)-len(master)*n)]
    key = []
    for i in range(len(random)):
        key.append(random[i]*ord(master[i]) % module)
    return key
