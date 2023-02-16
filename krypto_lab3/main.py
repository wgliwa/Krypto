# witold gliwa
import numpy as np
from PIL import Image

key = np.random.randint(0, 2, size=(64))
iv = np.random.randint(0, 2, size=(64))
B = np.array(Image.open('plain.bmp').convert("1"))
rows2, cols2 = B.shape
B = B[:rows2 - rows2 % 8, :cols2 - cols2 % 8]
A = B.flatten()
rows = A.shape
rows2, cols2 = B.shape
B = B.flatten()

for i in range(0, len(B), 64):
    B[i:i + 64] = B[i:i + 64] ^ key
tmp = []
for i in range(0, len(A), 64):
    if len(tmp):
        A[i:i + 64] = tmp ^ A[i:i + 64] ^ key
        tmp = A[i:i + 64]
    else:
        tmp = A[i:i + 64] ^ iv
        A[i:i + 64] = tmp
A = np.reshape(A, (rows2, cols2))
B = np.reshape(B, (rows2, cols2))
x = Image.fromarray(B)
x.save("ecb.bmp")
y = Image.fromarray(A)
y.save("cbc.bmp")
