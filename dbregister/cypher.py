"""
Created on Dec 23, 2013

@author: drifter
"""
import hashlib
import random


max_length = 16
padding = ''.join(chr(random.randint(0, 0xFF)) for i in range(max_length))


def xor(data, key):
    return bytearray([data[i] ^ key[i % len(key)] for i in range(len(data))])


def encode(data, key):
    padding_length = max_length - len(data)
    key = bytearray(key)
    data = bytearray(data.encode('utf-8'))
    data += bytearray(padding)[:padding_length - 1] + bytearray([padding_length])
    return xor(data, key)


def decode(data, key):
    key = bytearray(key)
    data = bytearray(data)
    data = xor(data, key)
    padding_length = data[-1]
    print padding_length
    data = data[:len(data) - padding_length]

    return data.decode('utf-8')


def create_key(*args):
    m = hashlib.sha256()
    m.update(''.join(args))
    return m.digest()[:16]
