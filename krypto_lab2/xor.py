# witold gliwa
import argparse
import os.path
from pathlib import Path


def prepare_text():
    if os.path.exists("orig.txt"):
        orig = Path("orig.txt").read_text().lower()
        orig = ''.join([i for i in orig if i.isalpha() or i.isspace()])
        if len(orig) < 64:
            print("text too short")
            return
        if len(orig) % 64 != 0:
            orig = orig[:-(len(orig) % 64)]
        parts = [orig[i:i + 64] for i in range(0, len(orig), 64)]
        f = open('plain.txt', 'w+')
        for i in parts:
            f.write(i + "\n")
    else:
        print("no files")


def cipher():
    if os.path.exists("orig.txt") and os.path.exists("key.txt"):
        plain = open("plain.txt").read().splitlines()
        key = open("key.txt").read()
        if len(key) < 64:
            print("key too short")
            return
        f = open("crypto.txt", "w+")
        for a in plain:
            for i, j in zip(a, key):
                f.write(hex(ord(i) ^ ord(j)) + " ")
    else:
        print("no files")


def cryptanalysis():
    if os.path.exists("crypto.txt"):
        crypto = open("crypto.txt", "r").read().split(' ')
        crypto = crypto[:-1]
        crypto = [crypto[i:i + 64] for i in range(0, len(crypto), 64)]
        key = [-1] * len(crypto[0])
        for i in range(len(crypto)):
            for j in range(len(crypto[i])):
                if int(crypto[i][j], 16) > ord('@'):
                    key[j] = int(crypto[i][j], 16) ^ ord(' ')
        result = crypto[:]
        for i in range(len(key)):
            if key[i] != -1:
                for j in range(len(crypto)):
                    result[j][i] = chr(int(crypto[j][i], 16) ^ key[i])
        de = open("decrypt.txt", "w+")
        for i in result:
            tmp = ""
            for j in i:
                if j.isalpha() or j.isspace():
                    tmp += j
                else:
                    tmp += '_'
            de.write(tmp + "\n")
    else:
        print("no files")

prepare_text()
cipher()
cryptanalysis()
# parser = argparse.ArgumentParser()
# parser.add_argument("-p", action='store_true')
# parser.add_argument("-e", action='store_true')
# parser.add_argument("-k", action='store_true')
# argument = parser.parse_args()
#
# if argument.p:
#     prepare_text()
# elif argument.e:
#     cipher()
# elif argument.k:
#     cryptanalysis()
# else:
#     print("huh")
