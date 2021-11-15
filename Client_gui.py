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
   
    r_and_v_crypt= encrypt(key, r_v)
    print(f"Зашифрованное сообщение: {r_and_v_crypt}")

    print("Отправляем зашифрованное сообщение Bob")
    connection.sendall(r_and_v_crypt)

    print("Отправляем ключ шифрования")
    key=key.encode()
    connection.sendall(key)

    print("Конец \n\n")
def Protocol_privazki_k_bity_Bob():
    # Отправка данных
    print("1)Получатель R(BOB) наугад равномерно выбирает r<{0,1}^n, и отправляет r отправителю |",end=' ')
    print("Bob выбирает бит или последовательность битов")

    event, values = window.read()
    text = values[1]
    print("Bob выбирает биты: "+text)
    message = text.encode()
    connection.sendall(message)

    #Принимаем зашифрованное сообщение от Alice
    data = connection.recv(1024)
    print(f"Зашифрованное сообщение от Alice: {data}")
            
    key=connection.recv(1024)
    key=key.decode()
    print(f"Alice передала ключ: {key}")

    print("Bob расшифровывает сообщение, узнавая бит, и проверяет свою случайную строку, убеждаясь в правильности бита.")
    print("Рассшифровка сообщения...")
    print("Расшифрованная строка : ",end=' ')
    r_and_v_decrypt = decrypt(key,data)
    print(str(r_and_v_decrypt).replace("'","").replace("b",""))

    print("Конец \n\n")

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

    print("Конец \n\n")
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

    print("Конец \n\n")


    print()

def Protocol_exponent_podbrasivaniy_monety_Alice():
    print("Алиса выбирает число X")
    event,values = window.read()
    x = values[1]
    x = int(x)

    print("g = 5, p = 3 (Фиксированные значения)")
    g=5
    p=3
    y=(g**x)%p

    print("y=g^x(mod p) | y="+str(y))
    print("Алиса отправляет число Бобу")

    y = str(y)
    y = y.encode()
    connection.sendall(y)

    print("Число передано, ждите ответа от Bob")

    data = connection.recv(1024)
    data = data.decode()

    print("Bob выбрал свои значения")
    print("Алиса выбирает случайный бит С (0 или 1) и отправляет его Бобу")
    event,values = window.read()
    c = values[1] 
    c = c.encode()
    connection.sendall(c)
    c = c.decode()

    print("Bob должен отправить свои значения b и k. Подождите...")
    data_b = connection.recv(1024)
    data_k = connection.recv(1024)
    b = data_b.decode()
    k = data_k.decode()

    print("Бит Bob = " + str(b))
    print("Бит Alice = " + str(c))
    print("Алиса проверяет что y=g^x(mod p). Если да то результат протокола будет бит d = b xor c")

    if int(y) == (g**x)%p:
        if int(b)== 0 and int(c)== 0:
            d=0
            print("d = "+str(d))
        elif int(b)== 1 and int(c)== 0:
            d=1
            print("d = "+str(d))
        elif int(b)== 0 and int(c)== 1:
            d=1
            print("d = "+str(d))
        elif int(b)== 1 and int(c)== 1:
            d=0
            print("d = "+str(d))
    else:
        print("Проверка не прошла")

    print("Конец \n\n")
def Protocol_exponent_podbrasivaniy_monety_Bob():
    print("Alice выбирает число и высчитывает значение y=g^x(mod p), подождите...")

    data = connection.recv(1024)
    data = data.decode()
    y = data
    print("y = "+ str(y))
    print("g = 5, p = 3 (Фиксированные значения)")
    g=5
    p=3

    print("Боб выбирает случайный бит (0 или 1)")
    event,values = window.read()
    b = values[1]

    print("Боб выбирает случайное число K")
    event,values = window.read()
    k = values[1]

    r=((int(y)**int(b))*(g**int(k)))%p
    print("r=y^b*g^k(mod p) | r="+ str(r))
    
    a = "1"
    a = a.encode()
    connection.sendall(a)

    print("Alice выбирает бит(0 или 1), Подождите...")
    data = connection.recv(1024)
    data = data.decode()

    print("Боб отправляет b и k Алисе")
    b = str(b)
    b = b.encode()
    k = str(k)
    k = k.encode()
    connection.sendall(b)
    connection.sendall(k)

    print("Конец \n\n")



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

        while True:
            print("Второй человек выбирает протокол и ваши роли в нем \n\n")
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

            elif protocol=='Экспоненциальный протокол подбрасывнания монеты':
                print("Выбрано: Экспоненциальный протокол подбрасывнания монеты")
                if roll == 'Alice':
                    print("Ваша роль: Bob")
                    Protocol_exponent_podbrasivaniy_monety_Bob()
                elif roll == 'Bob':
                    print("Ваша роль: Alice")
                    Protocol_exponent_podbrasivaniy_monety_Alice()

window.close()