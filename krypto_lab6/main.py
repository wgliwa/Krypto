import argparse


def encode():
    d = bin(int(open("mess.txt", 'r').read(), 16))[2:].zfill(16)
    with open("stegano.html", "a+").readlines() as h:
        for l in h:
            print(l)


def decode():
    pass


encode()

parser = argparse.ArgumentParser()
parser.add_argument("-k", action='store_true')
parser.add_argument("-e", action='store_true')
argument = parser.parse_args()
