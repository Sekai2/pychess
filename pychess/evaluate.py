#code for evaluation function

from misc import *

#function for counting the amount of material on the board
def countMaterial(board):
		count = []
		pieceChar = 'PNBRQKpnbrqk'
		for i in range(12):
			count.append(0)

		for i in board:
			if i != None:
				count[pieceChar.find(i.character)] += 1
		return count

#Evalutation code
class evaluate():
	def valSub(count, i):
		return count[i] - count[i + 6]

	def bishopPair(count):
		pairScore = 0
		if count[2] >= 2:
			if count[0] + count[6] >= 8:
				pairScore += ((16 - count[0]- count[6]) * 5) + 10

			else:
				pairScore += 50

		if count[8] >= 2:
			if count[0] + count[6] >= 8:
				pairScore -= ((16 - count[0]- count[6]) * 5) + 10

			else:
				pairScore -= 50

		return pairScore

    #material evaluation
	def material(count):
		multiplier = [100,350,350,525,1000,10000]
		materialScore = 0
		index = 0
		for i in multiplier:
			materialScore += i * evaluate.valSub(count, index)
			index += 1

		materialScore += evaluate.bishopPair(count)

		return materialScore

    #mobility evaluation
	def mobility(board):
		#each square has a value of 1. Can be increased to change scaling
		mobilityScore = 0
		#defining centre squares as they are weighted more
		#for speed some pawn structure features are also 
		#incorperated into mobility score
		centre = [0x33, 0x34, 0x43, 0x44]
		WpawnLocations = []
		BpawnLocations = []
		for i in board.board:
			if i != None:
				if i.colour == 'white':
					for j in i.ADSquares:
						if j in centre:
							mobilityScore += 3

						else:
							mobilityScore += 1

						if i.character == 'P':
							WpawnLocations.append(i.location)
							if board.board[j] != None:
								if board.board[j].character == 'P':
									mobilityScore += 2

                            #bonuses for pawn moves to centre
							if board.fullmove_clock < 10:
								if i.location in [0x43,0x44]:
									mobilityScore += 8
							
					if i.character == 'P':
						if board_rank(i.location) == 7:
							if board[i.location - 16] == None:
								mobilityScore += 1

							if board[i.location - 32] == None:
								mobilityScore += 1

				else:
					for j in i.ADSquares:
						if j in centre:
							mobilityScore -= 3

						else:
							mobilityScore -= 1

						if i.character == 'p':
							BpawnLocations.append(i.location)
							if board.board[j] != None:
								if board.board[j].character == 'p':
									mobilityScore -= 2

                            #bonuses for pawn moves to the centre
							if board.fullmove_clock < 10:
								if i.location in [0x33,0x34]:
									mobilityScore -= 8
								
					if i.character == 'p':
						if board_rank(i.location) == 0:
							if board[i.location + 16] == None:
								mobilityScore -= 1

							if board[i.location + 32] == None:
								mobilityScore -= 1

		mobilityScore += evaluate.pawnStruct(WpawnLocations)
		mobilityScore -= evaluate.pawnStruct(BpawnLocations)

		return mobilityScore

	#for pawn structure
	def pawnStruct(locations):
		isolatedFiles = 0
		missingFiles = [0,1,2,3,4,5,6,7]
		doubled_pawns = 0
		chains = []
		chainScore = 0
		ranks = []
		for i in range(30):
			chains.append(0)

		for i in locations:
			if board_file(i) in missingFiles:
				missingFiles.remove(board_file(i))

			else:
				doubled_pawns += 1

			chains[(board_rank(i) - board_file(i)) + 7] += 1
			chains[(board_rank(i) + board_file(i)) + 15] += 1

			if board_rank(i) not in ranks:
				ranks.append(i)

		for i in missingFiles:
			for j in missingFiles:
				if i - j == 2:
					if i - 1 not in missingFiles:
						isolatedFiles += 1

		for i in chains:
			if i > 1:
				chainScore += (i-1)*2

		maxRank1 = max(ranks)
		ranks.remove(maxRank1)
		maxRank2 = max(ranks)
		overextendScore = abs(maxRank2 - maxRank1)
		if overextendScore > 2:
			overextendScore = overextendScore * -10

		return (isolatedFiles * -1) + (doubled_pawns * -20) + chainScore + overextendScore

	#final evaluation
	def totalEval(board):
		return evaluate.material(board.materialCount) + evaluate.mobility(board)