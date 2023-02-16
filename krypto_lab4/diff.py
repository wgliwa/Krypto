# witold gliwa
import hashlib


def calc(a, b):
    total, diff = 0, 0
    for i, j in zip(bin(int(a, 16))[2:].zfill(len(a) * 4), bin(int(b, 16))[2:].zfill(len(b) * 4)):
        total += 1
        if i != j:
            diff += 1
    return f"liczba rozniacych sie bitow: {diff} z {total}, procentowo {round(float(diff / total) * 100)}%"


hash_functions = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b"]
p1, p2, pdf = open("personal.txt", "rb").read(), open("personal_.txt", "rb").read(), open("hash-.pdf", "rb").read()
with open("diff.txt", "w+") as h:
    for i in hash_functions:
        a, b = getattr(hashlib, i)(pdf + p1).hexdigest(), getattr(hashlib, i)(pdf + p2).hexdigest()
        h.write(f"{i}sum\n{a}\n{b}\n{calc(a, b)}\n\n")
