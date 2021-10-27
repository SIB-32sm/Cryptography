from typing import Text
import PySimpleGUI as sg
from simplecrypt import encrypt, decrypt
import random
import socket

h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

layout = [  
    [sg.Text('Выбор роли', size=(15, 1)), sg.InputCombo(('Alice', 'Bob'), size=(50, 3))],
    [sg.Text('Выбор протокола', size=(15, 1)), sg.InputCombo(("Привзяка к биту на основе симметричной криптографии","Протокол подбрасывания монеты"), size=(50, 3))],
    [sg.Submit(), sg.Cancel()], 
    [sg.Output(size=(88, 20))],
    [sg.Text('Поле ввода: '), sg.InputText(size=(71, 3)),sg.Submit('Ввод')]
        ]

window = sg.Window('Settings', layout)

def Protocol_privazki_k_bity_Alice():
    protocol = protokol.encode()
    roll = role.encode()
    connection.sendall(protocol)
    connection.sendall(roll)

    data = connection.recv(1024)

    data = data.decode()
    print(f"Bob выбрал биты : {data}")

    bit_from_bob=data
    text = 0
    
    print("Alice выбирает сообщение")
    event, values = window.read()
    text = values[2]

    print(f"Битовый текст Alice: {text}")
    r_v=text+bit_from_bob
    print(f"Текст Alice + Последовательность битов выбранная Bob: {r_v}")

    print("Шифрование AES-256. Введите ключ: ")
    event, values = window.read()
    key = values[2]
    
    print("Шифрование данных...\n")

    r_and_v_crypt= encrypt(key, r_v)
    print(f"Зашифрованное сообщение: {r_and_v_crypt}")

    print("Отправляем зашифрованное сообщение Bob")
    connection.sendall(r_and_v_crypt)

    print("Отправляем ключ шифрования")
    key=key.encode()
    connection.sendall(key)

    print("Конец")
def Protocol_privazki_k_bity_Bob():
    protocol = protokol.encode()
    roll = role.encode()
    connection.sendall(protocol)
    connection.sendall(roll)

    # Отправка данных
    print("1)Получатель R(BOB) наугад равномерно выбирает r<{0,1}^n, и отправляет r отправителю |",end=' ')
    print("Bob выбирает бит или последовательность битов")
    event, values = window.read()
    
    text = values[2]
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

    print("Конец")

while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        break

    if event == 'Submit':
        ip=IP_addres
        role=values[0]
        protokol=values[1]

        server_address = (ip, 10000)
        print('Старт сервера на {} порт {}'.format(*server_address))
        sock.bind(server_address)
        sock.listen(1)

        print("Протокол: " + values[2])
        print("Ваша роль: "+ values[1])

        print('Ожидание соединения...')
        connection, client_address = sock.accept()

        try:
            print('Подключено к:', client_address)

            if protokol =='Привзяка к биту на основе симметричной криптографии':
                    if role == 'Alice':
                        Protocol_privazki_k_bity_Alice()   
                    elif role == 'Bob':
                        Protocol_privazki_k_bity_Bob()

        finally:
            connection.close()

window.close()