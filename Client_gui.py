from typing import Text
import PySimpleGUI as sg
import socket
import sys
from simplecrypt import encrypt, decrypt
import random

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

layout = [  
    [sg.Text('Ip: '), sg.InputText(size=(71, 3)), sg.Submit('Подключится')],
    [sg.Output(size=(88, 30))],
    [sg.Text('Поле ввода: '), sg.InputText(size=(71, 3)),sg.Submit('Ввод')]
        ]

def Protocol_privazki_k_bity_Alice():
    print("Ваша роль : Alice")
    data = connection.recv(1024)
    data = data.decode()
    print(f'От Bob: {data}')
    print(f"Bob выбрал биты : {data}")

    bit_from_bob=data
    text = 0
    
    print("Alice выбирает сообщение")

    event, values = window.read()
    text = values[1]
    
    print(f"Битовый текст Alice: {text}")
    r_v=text+bit_from_bob
    print(f"Текст Alice + Последовательность битов выбранная Bob: {r_v}")

    print("Шифрование AES-256. Введите ключ: ")
    event, values = window.read()
    key = values[1]
    print()

    r_and_v_crypt= encrypt(key, r_v)
    print(f"Зашифрованное сообщение: {r_and_v_crypt}")

    print("Отправляем зашифрованное сообщение Bob")
    connection.sendall(r_and_v_crypt)

    print("Отправляем ключ шифрования")
    key=key.encode()
    connection.sendall(key)

    print("Конец \n")
def Protocol_privazki_k_bity_Bob():
    print("Ваша роль : Bob")
    # Отправка данных
    print("1)Получатель R(BOB) наугад равномерно выбирает r<{0,1}^n, и отправляет r отправителю |",end=' ')
    print("Bob выбирает бит или последовательность битов")

    event, values = window.read()
    text = values[1]
    print("Bob выбирает биты: "+text)
    message = text.encode()
    connection.sendall(message)

    print()

    #Принимаем зашифрованное сообщение от Alice
    data = connection.recv(1024)
    print(f"Зашифрованное сообщение от Alice: {data}")
            
    key=connection.recv(1024)
    key=key.decode()
    print(f"Alice передала ключ: {key}")

    print()
    print("Bob расшифровывает сообщение, узнавая бит, и проверяет свою случайную строку, убеждаясь в правильности бита.")
    print("Рассшифровка сообщения...")
    print("Расшифрованная строка : ",end=' ')
    r_and_v_decrypt = decrypt(key,data)
    print(str(r_and_v_decrypt).replace("'","").replace("b",""))

    print("Конец \n")

window = sg.Window('Settings', layout)

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Подключится':
        ip = values[0]

        server_address = (ip, 10000)
        print('Подключено к {} порт {}'.format(*server_address))
        connection.connect(server_address)

        print("Второй человек выбирает протокол и ваши роли в нем")
        protocol = connection.recv(1024).decode()
        roll = connection.recv(1024).decode()
        
        print("Протокол и роли выбраны \n")
        
        if protocol=='Привзяка к биту на основе симметричной криптографии':
            print("Выбрано: Протокол привязки к биту на основе симметричной криптографии")
            if roll == 'Alice':
                Protocol_privazki_k_bity_Bob()
            elif roll == 'Bob':
                Protocol_privazki_k_bity_Alice()

window.close()