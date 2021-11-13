from typing import Text
import PySimpleGUI as sg
import socket
from simplecrypt import encrypt, decrypt
import random

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

layout = [  
    [sg.Text('Ip: '), sg.InputText(size=(71, 3)), sg.Submit('Подключится')],
    [sg.Output(size=(88, 23))],
    [sg.Text('Поле ввода: '), sg.InputText(size=(71, 3)),sg.Submit('Ввод')]
        ]

def open_close(name):
    print(f'{name} создает пару открытый/закрытый ключ')
    print("Введите простые числа p и q.")

    print("Введите p")
    event,values = window.read()
    p = int(values[1])

    print("Введите q")
    event,values = window.read()
    q = int(values[1])

    n = p*q
    m = (p-1)*(q-1)
    print(f'Значение функции Эйлера для числа {n} = {m}')
    print(f'Числа взаимно простые с {m}')
    for b in range(2, m):
        num1 = m
        num2 = b
        while(num1 != num2):
            if(num1 < num2):
                temp = num1
                num1 = num2
                num2 = temp
            num1 -= num2
        if(num1 == 1):
            print(b, end=" ")
    print()
    print("Выберите число e из предложенных выше.\ne = ")
    event,values = window.read()
    e = int(values[1])
    for d in range(1, n):
        if((d*e)%m == 1):
            break
    return (n,e),(n,d)

def Protocol_privazki_k_bity_Alice():
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

def Protocol_podbrasivaniy_monety_Alice():
    print("1)Alice выбирает большое случайное целое число x") 
    event,values = window.read()
    x = int(values[1])
    
    y = x * 12345
    print("Вычисляем y=f(x) и сообщаем число y Бобу| y=x*12345 | y = "+str(y))
    y = str(y)
    y = y.encode()
    connection.sendall(y)

    data = connection.recv(1024)
    num = int(data.decode())

    print("Alice сообщает Bob о том, что его предположение правильно или нет, и называет ему число x.")
    
    if x % 2 == 0:
        print("Число Alice: "+str(x)+"  Оно четное")
        if num == 1:
            print("Боб угадал, он предположил что число четное")
        elif num == 0:
            print("Боб не угадал, он предположил что число нечетное")
    elif x % 2 == 1:
        print("Число Alice: "+str(x)+" Оно нечетное")
        if num == 1:
            print("Боб неугадал, он предположил что число четное")
        elif num == 0:
            print("Боб угадал, он предположил что число нечетное")

    x=str(x)
    x = x.encode()   
    connection.sendall(x)

    print("Конец")
def Protocol_podbrasivaniy_monety_Bob():
    print("Подождите пока Alice выбирает число (x) и высчитывает значение функции |y = x * 12345| ")

    data = connection.recv(1024)
    y = data.decode()
    
    print("Alice передала значение y=f(x), y = "+str(y))

    print("Bob сообщает Alice свое предположение о числе x: четное оно или нечетное. ")
    print("Введите свое предположение(1-Четное | 0-Нечетное)")
    event,values = window.read()
    num= values[1]
    predpolozhenie = num.encode()
    connection.sendall(predpolozhenie)

    data_x = connection.recv(1024)
    data_x = data_x.decode()
    x = int(data_x)

    num = int(num)
    print("Alice передает свое число: "+str(x))
    if x % 2 == 0:
        print("Число Alice: "+str(x)+"  Оно четное")
        if num == 1:
            print("Боб угадал, он предположил что число четное")
        elif num == 0:
            print("Боб не угадал, он предположил что число нечетное")
    elif x % 2 == 1:
        print("Число Alice: "+str(x)+" Оно нечетное")
        if num == 1:
            print("Боб неугадал, он предположил что число четное")
        elif num == 0:
            print("Боб угадал, он предположил что число нечетное")

    print("Alice назвала число и Bob проводит последнюю проверку")
    print("Bob проверяет, что y=f(x)")

    y1 = int(x)*12345

    if y1 == int(y):
        print("Все правильно, проверка пройдена")
    else:
        print("Проверка не пройдена, что то не так")

    print("Конец")


    print()

def Virtual_poker_Alice():
    print()
def Virtual_poker_Bob():
    print()

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
                print("Ваша роль: Bob")
                Protocol_privazki_k_bity_Bob()
            elif roll == 'Bob':
                print("Ваша роль: Alice")
                Protocol_privazki_k_bity_Alice()

        elif protocol=='Протокол подбрасывания монеты на основе однонаправленной функции':
            print("Выбрано: Протокол подбрасывания монеты на основе однонаправленной функции")
            if roll == 'Alice':
                print("Ваша роль: Bob")
                Protocol_podbrasivaniy_monety_Bob()
            elif roll == 'Bob':
                print("Ваша роль: Alice")
                Protocol_podbrasivaniy_monety_Alice()

        elif protocol=='Виртуальный покер':
            print("Выбрано: Виртуальный покер")
            if roll == 'Alice':
                print("Ваша роль: Bob")
                Virtual_poker_Bob()
            elif roll == 'Bob':
                print("Ваша роль: Alice")
                Virtual_poker_Alice()

window.close()
