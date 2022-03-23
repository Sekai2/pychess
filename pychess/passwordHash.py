import time

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
def hash(password):
	numbers = PRNG.LCG(len(password), 257991014)
	h = 0
	for i in range(len(password)):
		h = h ^ ord(password[i]) ^ numbers[i]
	return h

print(hash('fjughgibi .. bhlbfg jepg983  jgjgb j  rtjhi '))
