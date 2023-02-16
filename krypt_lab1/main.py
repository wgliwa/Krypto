# witold gliwa
import argparse
import os.path
from pathlib import Path


def is_in_english(file):
    try:
        file.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def cesar_cipher():
    if os.path.exists("plain.txt") and os.path.exists("key.txt"):
        plain = Path("plain.txt").read_text()
        try:
            key = int(Path("key.txt").read_text())
        except ValueError:
            print("wrong key")
        else:
            if is_in_english(plain) and all(char.isalpha() or char.isspace() for char in plain):
                result = ""
                for i in plain:
                    if i.isupper():
                        result += chr((ord(i) + key - 65) % 26 + 65)
                    elif i.isalpha():
                        result += chr((ord(i) + key - 97) % 26 + 97)
                    else:
                        result += i
                open("crypto.txt", "w+").write(result)
            else:
                print("plain text contains forbidden characters")

    else:
        print("no files")


def cesar_key_decipher():
    if os.path.exists("crypto.txt") and os.path.exists("key.txt"):
        crypto = Path("crypto.txt").read_text()
        try:
            key = int(Path("key.txt").read_text())
        except ValueError:
            print("wrong key")
        else:
            if is_in_english(crypto) and all(char.isalpha() or char.isspace() for char in crypto):
                result = ""
                for i in crypto:
                    if i.isupper():
                        result += chr((ord(i) - key - 65) % 26 + 65)
                    elif i.isalpha():
                        result += chr((ord(i) - key - 97) % 26 + 97)
                    else:
                        result += i
                open("decrypt.txt", "w+").write(result)
            else:
                print("crypted text contains forbidden characters")

    else:
        print("no files")


def cesar_text_decipher():
    if os.path.exists("crypto.txt") and os.path.exists("extra.txt"):
        extra = Path("extra.txt").read_text()
        crypto = Path("crypto.txt").read_text()
        if (is_in_english(crypto) and all(char.isalpha() or char.isspace() for char in crypto)) and (
                is_in_english(extra) and all(char.isalpha() or char.isspace() for char in extra)):
            key = (ord(crypto[0]) - ord(extra[0])) % 26
            for i, j in zip(crypto, extra):
                if i.isupper() and (ord(i) - key - 97) % 26 != (ord(j) - 97) % 26:
                    print("cant calculate the key")
                    return
                elif i.isalpha() and (ord(i) - key - 65) % 26 != (ord(j) - 65) % 26:
                    print("cant calculate the key")
                    return
            result = ""
            for i in crypto:
                if i.isupper():
                    result += chr((ord(i) - key - 65) % 26 + 65)
                elif i.isalpha():
                    result += chr((ord(i) - key - 97) % 26 + 97)
                else:
                    result += i
            open("decrypt.txt", "w+").write(result)
            open("key-found.txt", "w+").write(str(key))
        else:
            print("error in files")
    else:
        print("no files")


def ceasar_guesser():
    if os.path.exists("crypto.txt"):
        crypto = Path("crypto.txt").read_text()
        if is_in_english(crypto) and all(char.isalpha() or char.isspace() for char in crypto):
            result = ""
            for i in range(1, 26):
                tmp = ""
                for j in crypto:
                    if j.isupper():
                        tmp += chr((ord(j) + i - 65) % 26 + 65)
                    elif j.isalpha():
                        tmp += chr((ord(j) + i - 97) % 26 + 97)
                    else:
                        tmp += j
                result += tmp + "\n"
            open("decrypt.txt", "w+").write(result)
            print("saved result to decrypt.txt")
        else:
            print("error in files")
    else:
        print("no files")


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


def affine_cipher():
    if os.path.exists("plain.txt") and os.path.exists("key.txt"):
        plain = Path("plain.txt").read_text()
        key = Path("key.txt").read_text()
        try:
            keya = int(key[0])
            keyb = int(key[2])
        except ValueError:
            print("wrong key")

        else:
            if modinv(keya, 26):
                if is_in_english(plain) and all(char.isalpha() or char.isspace() for char in plain):
                    result = ""
                    for i in plain:
                        if i.isupper():
                            result += chr((keya * (ord(i) - 65) + keyb) % 26 + 65)
                        elif i.isalpha():
                            result += chr((keya * (ord(i) - 97) + keyb) % 26 + 97)
                        else:
                            result += i
                    open("crypto.txt", "w+").write(result)
                else:
                    print("plain text contains forbidden characters")
    else:
        print("no files")


def affine_key_decipher():
    if os.path.exists("crypto.txt") and os.path.exists("key.txt"):
        crypto = Path("crypto.txt").read_text()
        key = Path("key.txt").read_text()
        try:
            keya = int(key[0])
            keyb = int(key[2])
        except ValueError:
            print("wrong key")

        else:
            if modinv(keya, 26):
                if is_in_english(crypto) and all(char.isalpha() or char.isspace() for char in crypto):
                    result = ""
                    for i in crypto:
                        if i.isupper():
                            result += chr((modinv(keya, 26) * (ord(i) - 65 - keyb)) % 26 + 65)
                        elif i.isalpha():
                            result += chr((modinv(keya, 26) * (ord(i) - 97 - keyb)) % 26 + 97)
                        else:
                            result += i
                    open("decrypt.txt", "w+").write(result)
                else:
                    print("crypted text contains forbidden characters")

    else:
        print("no files")


def affine_text_decipher():
    if os.path.exists("crypto.txt") and os.path.exists("extra.txt"):
        extra = Path("extra.txt").read_text()
        crypto = Path("crypto.txt").read_text()
        if (is_in_english(crypto) and all(char.isalpha() or char.isspace() for char in crypto)) and (
                is_in_english(extra) and all(char.isalpha() or char.isspace() for char in extra)):
            leng = len(extra)
            for i in range(1, 26):
                for j in range(26):
                    if modinv(i, 26):
                        tmp = ""
                        for k in extra:
                            if k.isupper():
                                tmp += chr((i * (ord(k) - 65) + j) % 26 + 65)
                            elif k.isalpha():
                                tmp += chr((i * (ord(k) - 97) + j) % 26 + 97)
                            else:
                                tmp += i
                        if crypto[:leng] == tmp:
                            open("key-found.txt", "w+").write(str(i) + " " + str(j))
                            return
        else:
            print("error in files")
    else:
        print("no files")


def affine_guesser():
    if os.path.exists("crypto.txt"):
        crypto = Path("crypto.txt").read_text()
        if is_in_english(crypto) and all(char.isalpha() or char.isspace() for char in crypto):
            result = ""
            for i in range(1, 26):
                for j in range(26):
                    if modinv(i, 26):
                        print(i, j)
                        tmp = ""
                        for k in crypto:
                            if k.isupper():
                                tmp += chr((modinv(i, 26) * (ord(k) - 65 - j)) % 26 + 65)
                            elif k.isalpha():
                                tmp += chr((modinv(i, 26) * (ord(k) - 97 - j)) % 26 + 97)
                            else:
                                tmp += k
                        result += tmp + "\n"
            open("decrypt.txt", "w+").write(result)
            print("saved result to decrypt.txt")
        else:
            print("error in files")
    else:
        print("no files")


parser = argparse.ArgumentParser()
parser.add_argument("-c", action='store_true')
parser.add_argument("-a", action='store_true')

parser.add_argument("-e", action='store_true')
parser.add_argument("-d", action='store_true')
parser.add_argument("-j", action='store_true')
parser.add_argument("-k", action='store_true')
argument = parser.parse_args()
if argument.c:
    if argument.e:
        cesar_cipher()
    elif argument.d:
        cesar_key_decipher()
    elif argument.j:
        cesar_text_decipher()
    elif argument.k:
        ceasar_guesser()
    else:
        print("what?")
elif argument.a:
    if argument.e:
        affine_cipher()
    elif argument.d:
        affine_key_decipher()
    elif argument.j:
        affine_text_decipher()
    elif argument.k:
        affine_guesser()
    else:
        print("what?")
else:
    print("what?")
