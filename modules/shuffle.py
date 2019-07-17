from math import sqrt

def gen_shuffle(data):
    num=len(data)
    razbros,itog=int(sqrt(num)),[-1 for i in range(num)]
    for i in range(num): itog[(i+i*razbros)%num]=data[i]
    return itog
    