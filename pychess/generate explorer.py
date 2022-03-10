import chess
class startBoard():
	def __init__(self, FEN):
		self.FEN = FEN
		self.moves = []
		self.count = 0

	def filter1(self):
		board = chess.Board(self.FEN)
		missing = list(board.legal_moves)
		self.count = len(missing)
		for i in self.moves:
			if chess.Move.from_uci(i) in missing:
				missing.remove(chess.Move.from_uci(i))

		return missing

f = open('generated.txt','r')
listAll = f.read().splitlines()
f.close()

FENBoards = []
FENBoardsBoards = []
for i in range(len(listAll)):
	if i % 2 == 0:
		if listAll[i] not in FENBoardsBoards:
			FENBoardsBoards.append(listAll[i])
			FENBoards.append(startBoard(listAll[i]))
			FENBoards[FENBoardsBoards.index(listAll[i])].moves.append(listAll[i + 1])

		else:
			FENBoards[FENBoardsBoards.index(listAll[i])].moves.append(listAll[i + 1])

f = open('badBoard.txt','a')
count = 0
for i in FENBoards:
	a = i.filter1()
	if len(a) != 0:
			for j in a:
				f.write(i.FEN)
				f.write('\n')
				f.write(str(j))
				f.write('\n')

	count += i.count

f.close()

print(count)
print('finished')
input()