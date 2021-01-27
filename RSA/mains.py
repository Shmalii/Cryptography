from Body import *
import requests



class Body:#клас людина
    e=''
    n=''
    __d = ''
    __p = ''
    __q = ''
    S=''
    __k_secret=''
    k_open =''

    def __init__(self):#конструктор за замовчуванням
        self.__k_secret= randint(1000,9999)


    def GENOPENKEY(self,length):#генерування ключа
        keylist = generatekeys(length)
        self.e = keylist[2]
        self.n = keylist[4]
        self.__q = keylist[1]
        self.__p = keylist[0]
        self.__d = keylist[3]

    def CREATEMESSAGE(self, e1, n1): #створення повіломелення на основі відкритого ключа іного користувача
        self.__k_secret = randint(1000, 9999)#генерування повідомлення
        k1 = encrypt(self.__k_secret,e1,n1)
        self.S= signature(self.__k_secret,self.__d, self.n)
        S1 = signature(self.S,e1,n1)
        print("Key e: ", hex(self.e))
        print("Key n: ", hex(self.n))
        print("Secret message: ", hex(self.__k_secret))
        print("Encrypted message: ", hex(k1))
        print("Signature: ", hex(self.S))
        return (k1,S1)

    def VERIFY(self, MSG, e1, n):#перевірка повідомлення та підпису
        k = decrypt(MSG[0],self.__d,self.n)
        S= signature(MSG[1],self.__d,self.n)
        kcheck = decrypt(S,e1,n)
        if k == kcheck:
            print("\n\nVerified!!!")
        else:
            print("\n\nOops, something went wrong")

        print("Key e: ", hex(self.e))
        print("Key n: ", hex(self.n))
        print("Encrypted message: ", hex(MSG[0]))
        print("Decrypted message: ", hex(k))
        print("Signature: ", hex(S))


class Hacker:#клас хакер
    e = ''
    n = ''
    __d = ''
    __p = ''
    __q = ''
    S = ''
    __k_secret = ''
    k_open = ''

    def __init__(self):#конструктор за замовчуванням
        self.__k_secret = randint(1000, 9999)

    def GENOPENKEY(self,length):#генерування ключа
        keylist = generatekeys(length)
        self.e = keylist[2]
        self.n = keylist[4]
        self.__q = keylist[1]
        self.__p = keylist[0]
        self.__d = keylist[3]

    def CREATEMESSAGE(self): #підміна повідомлення
        k1 = encrypt(self.__k_secret, self.e, self.n)
        self.S = signature(self.__k_secret, self.__d, self.n)
        S1 = signature(self.S, self.e, self.n)
        print("\n\n--------------__HACKER__----------------")
        print("Key e: ", hex(self.e))
        print("Key n: ", hex(self.n))
        print("Secret message: ", hex(self.__k_secret))
        print("Signature: ", hex(self.S))
        print("Encrypted message hacker: ", hex(k1))
        return (k1, S1)

while True:
    func = int(input("\n\nEnter 1 to local connection, 2 to connection with server: "))
    if func==1:
        #створення об'єктів абонентів та хакера
        bodyA = Body()
        bodyB = Body()
        bodyC = Hacker()
        #генерування ключів
        bodyC.GENOPENKEY(256)
        bodyB.GENOPENKEY(256)
        bodyA.GENOPENKEY(256)
        while bodyB.n < bodyA.n:#генерування ключа А, поки він не задовільнить умову
            bodyA.GENOPENKEY(256)
        k = randint(0,30)
        print("\n\n---------__PERSON A__----------")
        msg = bodyA.CREATEMESSAGE(bodyB.e,bodyB.n)#створення повідомлення
        if k % 3 == 0 or k % 4 == 0:
            msg = bodyC.CREATEMESSAGE()
        print("\n\n---------__PERSON B__----------")
        bodyB.VERIFY(msg, bodyA.e, bodyA.n)#верифікування повідомлення
    if func==2:
        bodyA = Body()
        bodyA.GENOPENKEY(256)
        print("\n\n--------------------Connect with server-----------------------")
        #під'єднання до тестового середовища
        link =f"http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize=300"#посилання на тестове середовище
        keysrequest = requests.get(link)#запит на отримання ключів
        servern = int(keysrequest.json()["modulus"],16)#отримання ключа n
        servere = int(keysrequest.json()["publicExponent"],16)#отримання ключа е
        print("Server keys: ", "n: ", hex(servern), "\ne: ", hex(servere))#вивід ключів у 16-ій системі
        print("\n\n---------__PERSON A__----------")
        mess = bodyA.CREATEMESSAGE(servere,servern)#створення повідомлення
        sendmsg = f"http://asymcryptwebservice.appspot.com/rsa/receiveKey?key={hex(mess[0])[2:]}&signature={hex(mess[1])[2:]}" \
                  f"&modulus={hex(bodyA.n)[2:]}&publicExponent={hex(bodyA.e)[2:]}"
        verifyrequest = requests.get(sendmsg, cookies=keysrequest.cookies)#посилання на сервер даних(повідомлення та підпису)
        msg = verifyrequest.json()["key"]#отримання розкодованого повідомлення
        status = verifyrequest.json()["verified"]#отримання результату верифікації
        print("Decrypted message: " + str(msg) + "\nServer said: " + str(status))