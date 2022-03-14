import time

class PRNG():
	def __init__(self, seed = int(time.time_ns())):
		self.seed1 = seed
		self.seedn = seed

	#Linear Conguential Generator
	def LCG(maxn = 1, seedn = int(time.time_ns()), m = 2147483647, a = 16807, c = 1, n = 0, result = []):
		if n == maxn:
			return result
		randnum = (a * seedn + c) % m
		result.append(randnum)
		return(PRNG.LCG(maxn, randnum, m, a, c, n + 1, result))

print(PRNG.LCG(100))