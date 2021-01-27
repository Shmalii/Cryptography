import math
from random import *
import datetime


def gcd(a,b):
    # Пошук НСД
    if a == 0:
        return b
    if a > b:
        tmp = a
        a = b
        b = tmp
    return gcd(b%a, a)


def Converse(mod, number):
    # пошук оберненого за модулем
    if number == 0:
        return mod, 1, 0
    d, x, y = Converse(number, mod % number)
    return d, y, x - (mod // number) * y


def check_first_prime(p):# перевіряємо перші 100 простих чисел
    for i in range(3,100,2):
        if p%i == 0:
            return True
    return False


def Gorner(x,d,p):#схема горнера для пошуку великих степенів за модулем
    binnary = bin(d)[2:]
    power = 1
    for i in range(len(binnary)):
        power = power**2%p
        power = (power * (x**(int(binnary[i]))))%p
    return power


def power2(d):
    s=0
    while d % 2 == 0:
        s += 1
        d //= 2
    return s


def Miller_rabin(p):
    for i in range(3,100,2):
        if p%i == 0:
            return False
    file = open('report.txt', 'a', encoding='utf-8')
    file.write("\n"+str(datetime.datetime.now())+"\n")
    k = 200
    temp = p-1
    d = temp
    s= power2(d)
    for i in range(k):
        x = randint(100, p-1)# генеруємо незалежне псевдовипадкове число
        if gcd(x,p)>1:# якщо НСД не 1
            file.write(str(p)+'  has divisors\n')
            return False
        else:
            xr = Gorner(x, d, p)#підносимо до степеня
            if xr == 1 or xr == p - 1:#сильно псевдопросте
                continue#переходимо до наступного кроку циклу
            for r in range(1, s):# крок 2.2
                xr = pow(xr,2,p)
                if xr == p - 1:#сильно псевдопросте
                    break
                elif xr == 1:
                    file.write(str(hex(p))+" is not pseudo-prime\n")
                    return False
            file.write(str(hex(p)) + " is not pseudo-prime\n")
            return False
    file.write(str(hex(p)) + " is pseudo-prime\n")
    file.close()
    return True


def randnum(minlim, maxlim):#пошук псевдовипадкового числа
    return randint(minlim,maxlim)


def find_prime(length):#пошук простого
    min = 2 ** length
    max = 2 ** (length + 1) - 1
    temp = randnum(min, max)
    temp = temp-1 if temp % 2 == 0 else temp
    while check_first_prime(temp):
        temp += 2
    while not Miller_rabin(temp):
        temp+=2
    return temp

def generatekeys(keylen):#генерування ключа
    min = 2**keylen
    max = 2**(keylen+1)-1
    keyp = 0
    keyq = 0
    e = pow(2,16) + 1
    while not min <= keyp*keyq <= max:
        keyp = find_prime(keylen // 2)
        keyq = find_prime(keylen // 2)
    n = keyq*keyp
    q = (keyp-1)*(keyq-1)
    d = Converse(q,e)[2]%q
    return (keyp, keyq, e, d, n)

def encrypt(M, e, n):#шифрування
    C = Gorner(M,e,n)
    return C


def decrypt(C,d,n):#розшифрування
    M = Gorner(C,d,n)
    return M


def signature(M,d,n):#підпис
    S = Gorner(M,d,n)
    return S