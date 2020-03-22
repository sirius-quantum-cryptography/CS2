__author__ = "nikikust"

from math import sqrt


def gen_shuffle(data):
    num = len(data)
    spread, result = int(sqrt(num)), [-1 for i in range(num)]
    for i in range(num):
        result[(i + i * spread) % num] = data[i]
    return result
