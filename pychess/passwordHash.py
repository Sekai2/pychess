import time
from misc import *

class PRNG():
	def __init__(self, seed = int(time.time_ns())):
		self.seed1 = seed
		self.seedn = seed

	#Linear Conguential Generator
	#default is random 31 bit number
	def LCG(maxn = 1, seedn = int(time.time_ns()), m = 2147483647, a = 16807, c = 1, n = 0, result = []):
		if n == maxn:
			return result

		elif n == 0:
			result = []
		randnum = (a * seedn + c) % m
		result.append(randnum)
		return(PRNG.LCG(maxn, randnum, m, a, c, n + 1, result))

	def LCGbetween(lower1, upper1, maxn = 1, seedn = int(time.time_ns())):
		rand_range = upper1 - lower1
		a = (upper1 + lower1)//2
		return LCG(maxn, seedn, rand_range, a, lower1)

#password hash
#def hash(password):
#	numbers = PRNG.LCG(len(password), 257991014)
#	h = 0
#	for i in range(len(password)):
#		h = h ^ ord(password[i]) ^ numbers[i]
#	return h

def sha2(password):
	h0 = 0x6a09e667
	h1 = 0xbb67ae85
	h2 = 0x3c6ef372
	h3 = 0xa54ff53a
	h4 = 0x510e527f
	h5 = 0x9b05688c
	h6 = 0x1f83d9ab
	h7 = 0x5be0cd19

	k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
	0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
	0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
	0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
	0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
	0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
	0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
	
	get_bin = lambda x, n: format(x,'b').zfill(n)

	val = ''
	for i in password:
		val += get_bin(ord(i), 8)

	length = len(val)

	val += '1'

	while len(val) % 512 != 448:
		val += '0'

	val += get_bin(length, 64)

	chunks = []
	for i in range(len(val)//512):
		chunks.append(val[i * 512: (i + 1) * 512])

	for chunk in chunks:
		w = []
		for i in range(64):
			w.append(0)

		for i in range(len(val)//32):
			w[i] = int(val[i * 32: (i+1) * 32] , 2)

		for i in range(16,64):
			s0 = (rightRotate(w[i-15], 7)) ^ (rightRotate(w[i-15], 18)) ^ (w[i-15] >> 3)
			s1 = (rightRotate(w[i-2], 17)) ^ (rightRotate(w[i-2], 19)) ^ (w[i-2] >> 10)
			w[i] = w[i - 16] + s0 + w[i-7] + s1

		a = h0
		b = h1
		c = h2
		d = h3
		e = h4
		f = h5
		g = h6
		h = h7


		for i in range(64):
			S1 = (rightRotate(e, 6)) ^ (rightRotate(e, 11)) ^ (rightRotate(e, 25))
			ch = (e & f) ^ ((~e) & g)
			temp1 = h + S1 + ch + k[i] + w[i]
			S0 = (rightRotate(a, 2)) ^ (rightRotate(a, 13)) ^ (rightRotate(a, 22))
			maj = (a & b) ^ (a & c) ^ (b & c)
			temp2 = S0 + maj

			h = g
			g = f
			f = e
			e = d + temp1
			d = c
			c = b
			b = a
			a = temp1 + temp2

		h0 = h0 + a
		h1 = h1 + b
		h2 = h2 + c
		h3 = h3 + d
		h4 = h4 + e
		h5 = h5 + f
		h6 = h6 + g
		h7 = h7 + h

	hashed = get_bin(h0, 32) + get_bin(h1, 32) + get_bin(h2, 32) + get_bin(h3, 32) + get_bin(h4, 32) + get_bin(h5, 32) + get_bin(h6, 32) + get_bin(h7, 32)

	# for i in range(len(val)//64):
	# 	a = ''
	# 	for j in range(64):
	# 		if j % 8 == 0:
	# 			a += ' '
	# 		a += val[i * 64 + j]

	# 	print(a)

	# print(len(val))
	hashed = int(hashed, 2)



	return hashed

if __name__ == '__main__':
	print(hex(sha2('hello world')))

