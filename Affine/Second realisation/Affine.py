import numpy as np

file= open('12.txt', 'r', encoding="utf-8")#12.txt
rus = "абвгдежзийклмнопрстуфхцчшщьыэюя"
poprus = ['ст','но','то','на','ен','ов','ни','ра','во','ко']

def gcd(x,y):
    while (y):
        x, y = y, x % y
    return x


def Euclid(mod, number):
    if number == 0:
        return mod, 1, 0
    d, x, y = Euclid(number, mod % number)
    return d, y, x - (mod // number) * y


def solving(n1,n2, mod):
    check = gcd(n1, mod)
    if check == 1 or gcd(n2,check) == check:
        obern= Euclid(n1/check, mod/check)[1]
        A =  (obern*n2/check) % (mod/check)
        return A, check
    else:
        return -1, check
text = file.read().replace('\n', '')
bigram = list()
ambigr= dict()
for a in range(0, len(text), 2):
    bigram.append(text[a:a+2])
for a in bigram:
    if a in ambigr:
        ambigr[a]+=1
    else:
        ambigr[a]=1
copybigr = dict(ambigr)
amount = 10
max = 0
maxind = 0
popular = dict()
for a in range(amount):
    for elem in copybigr:
        if copybigr[elem] > max:
            max = copybigr[elem]
            maxind = elem
    popular[maxind] = rus.index(maxind[0])*len(rus)+rus.index(maxind[1])
    copybigr[maxind] = -1
    max =0
poprusb = dict()
for elem in poprus:
    poprusb[elem] = rus.index(elem[0])*len(rus)+rus.index(elem[1])
for elem in ambigr:
    ambigr[elem]=rus.index(elem[0])*len(rus)+rus.index(elem[1])
keys = list(list())
popularlist = list(popular.keys())
for i in range(amount):
    for j in range(i, amount):
        for k in range(amount):
            n1 = poprusb[poprus[i%amount]]- poprusb[poprus[j%amount]]
            n2 = popular[popularlist[k%amount]]-popular[popularlist[(k+1)%amount]]
            mod = len(rus)**2
            a, nsd = solving(n1, n2, mod)
            if a!=-1:
                b =(popular[popularlist[k%amount]]-a* poprusb[poprus[i%amount]])%(mod/nsd)
                keys.append((int(a),int(b)))
        for k in range(10):
            n1 = poprusb[poprus[i%amount]]- poprusb[poprus[j%amount]]
            n2 = popular[popularlist[(k+1)%amount]]-popular[popularlist[(k)%amount]]
            mod = len(rus)**2
            a, nsd = solving(n1, n2, mod)
            if a!=-1:
                b =(popular[popularlist[(k+1)%amount]]- a* poprusb[poprus[i%amount]])%(mod/nsd)
                keys.append((int(a),int(b)))
impossible =  ['оь','аь','иь','уь','оь','гщ','щф','щх','щц','щй','щч','щш','щщ']
out = open('write.txt', 'w')
chck = True
for key in keys:
    decrypted = ''
    leng = len(rus)**2
    conv = Euclid(leng, key[0])[2]
    for elem in bigram:
        numb = (conv * (ambigr[elem]- key[1]))%leng
        decrypted += rus[numb//len(rus)]+rus[numb%len(rus)]
    for el in impossible:
        chck = True
        if el in decrypted:
            print(key, '---->', 'Has impossible bigram ', el)
            out.write(str(key)+'---->'+'has impossible bigram '+ el+'\n')
            chck = False
            break
    if chck==False:
        continue
    else:
        arr= []
        for elem in rus:
            arr.append(decrypted.count(elem)/len(decrypted))
        entr = (-1) * np.sum(arr * np.log2(arr))
        if 4.4<=entr<=4.6:
            print(key, '----->', 'Correct entropy ', entr)
            out.write(str(key)+ '----->'+ 'Correct entropy '+ str(entr)+'\n')
            print(decrypted)
            break
        else:
            print(key, '----->', 'incorrect entropy ', entr )
            out.write(str(key) + '----->' + 'incorrect entropy '+str(entr)+'\n')
open('decrypt.txt', 'w').write(decrypted)