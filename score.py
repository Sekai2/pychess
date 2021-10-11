#Elo Calculation
def expectedScore(Ra, Rb):
	Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
	return Ea

def updateElo(Ra, Sa, Ea):
	CONST_K = 34
	NewRa = Ra + CONST_K * (Sa - Ea)
	return NewRa

def score_change(piece1, piece2):
	return piece2.value