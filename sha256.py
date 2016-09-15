#!/usr/bin/python
#-*- coding: utf-8 -*-
# Author: Mathieu Tortuyaux 13 / 09 / 16

from hashlib import sha256

K = [
0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

H = [
0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

W = []

a = H[0]
b = H[1]
c = H[2]
d = H[3]
e = H[4]
f = H[5]
g = H[6]
h = H[7]

# DEFINITION DES FONCTIONS

ch = lambda x, y, z: ((x and y) + (not x and z)) % pow(2, 32)
maj = lambda x, y, z: ((x and y ) + (x and y) + (y and z)) % pow(2, 32)
rotate = lambda x, y: (x >> y) or ( x << (32 - y)) % pow(2, 32)
SIG0 = lambda x: (rotate(x, 2) + rotate(x, 13) + rotate(x, 22))%pow(2, 32)
SIG1 = lambda x: (rotate(x, 6) + rotate(x, 11) + rotate(x, 25))%pow(2, 32)
sig0 = lambda x: (rotate(x, 7) + rotate(x, 18) + x >> 3)%pow(2, 32)
sig1 = lambda x: (rotate(x, 17) + rotate(x, 19) + x >> 10)%pow(2,32)

def padding(word):
	
	pad = ""
	for f in word:
		pad += format(ord(f), 'b').zfill(8)

	clearLen = len(pad)

	zeros = 448 - (len(pad) + 1)
	pad += "1"
	pad += "0"*zeros
	pad += format(clearLen, 'b').zfill(64)
	return int(pad, 2)

def parsing(pad):

	m = []
	pad = str(format(pad, 'b'))

	for i in range(0, 512, 32):
		m.append(int(pad[i:i+32][::-1], 2))#big endian conversion
	return m


if __name__ == "__main__":

	pad = padding("abc")
	m = parsing(pad)

	for f in range(0, 16):
		W.append(m[f])

	for f in range(16, 64):
		W.append(sig1(W[f-2]) + W[f-7] + sig0(W[f-15]) + W[f-16])

	for t in range(0, 64):
		#print('%s : %s | %s | %s | %s | %s | %s | %s | %s'%(t, format(a, 'x').zfill(8), format(b, 'x').zfill(8), format(c, 'x').zfill(8), format(d, 'x').zfill(8), format(e, 'x').zfill(8), format(f, 'x').zfill(8), format(g, 'x').zfill(8), format(h, 'x').zfill(8)))

		T1 = h + SIG1(e) + ch(e, f, g) + K[t] + W[t]
		T2 = SIG0(a) + maj(a, b, c)
		h = g
		g = f
		f = e
		e = d + T1
		d = c
		c = b
		b = a
		a = T1 + T2
	
	H[0] = (a + H[0])%pow(2,32)
	H[1] = (b + H[1])%pow(2,32)
	H[2] = (c + H[2])%pow(2,32)
	H[3] = (d + H[3])%pow(2,32)
	H[4] = (e + H[4])%pow(2,32)
	H[5] = (f + H[5])%pow(2,32)
	H[6] = (g + H[6])%pow(2,32)
	H[7] = (h + H[7])%pow(2,32)

	hexdigest = ""

	real = sha256('abc').hexdigest()
	print(real, len(real))

	for f in H:

		print(hex(f))
	print(len(hexdigest))
	print(len(H))
