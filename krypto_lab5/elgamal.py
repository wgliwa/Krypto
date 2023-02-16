# witold gliwa
import argparse
from random import randint
from math import gcd
from re import findall


def generate_keys():
    p, g = map(int, open("elgamal.txt", 'r').read().splitlines())
    a = randint(1, p - 2)
    b = pow(g, a, p)
    open("private.txt", "w+").write(f"{p}\n{g}\n{a}")
    open("public.txt", "w+").write(f"{p}\n{g}\n{b}")


def encrypt():
    p, g, b = map(int, open("public.txt", 'r').read().splitlines())
    m = int("".join(str(ord(char)) for char in open("plain.txt", 'r').read()))
    if m > p:
        print("plain za dlugi")
        return
    k = coprime(p)
    c1 = pow(g, k, p)
    c2 = m * pow(b, k, p)
    open("crypto.txt", "w+").write(f"{c1}\n{c2}")


def decrypt():
    c1, c2 = map(int, open("crypto.txt", 'r').read().splitlines())
    p, g, a = map(int, open("private.txt", 'r').read().splitlines())
    reg = '[01]?\d\d'
    open("decrypt.txt", "w+").write(f"{''.join(map(chr, map(int, findall(reg, str((c2 * pow(c1, -a, p)) % p)))))}")


def signature():
    p, g, a = map(int, open("private.txt", 'r').read().splitlines())
    m = int("".join(str(ord(char)) for char in open("message.txt", 'r').read()))
    k = coprime(p - 1)
    r = pow(g, k, p)
    x = pow(k, -1, p - 1) * (m - a * r) % (p - 1)
    open("signature.txt", "w+").write(f"{r}\n{x}")


def verify():
    p, g, b = map(int, open("public.txt", 'r').read().splitlines())
    m = int("".join(str(ord(char)) for char in open("message.txt", 'r').read()))
    r, x = map(int, open("signature.txt", 'r').read().splitlines())
    res = 'T' if pow(g, m, p) == (pow(b, r, p) * pow(r, x, p)) % p else 'N'
    print(res)
    open("verify.txt", "w+").write(res)


def coprime(p):
    while 1:
        r = randint(2, p)
        if gcd(r, p) == 1:
            return r


parser = argparse.ArgumentParser()
parser.add_argument("-k", action='store_true')
parser.add_argument("-e", action='store_true')
parser.add_argument("-d", action='store_true')
parser.add_argument("-s", action='store_true')
parser.add_argument("-v", action='store_true')
argument = parser.parse_args()
if argument.k:
    generate_keys()
elif argument.e:
    encrypt()
elif argument.d:
    decrypt()
elif argument.s:
    signature()
elif argument.v:
    verify()
else:
    print("huh")
