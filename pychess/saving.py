import sqlite3
import json

#code for saving games
class save():
	def __init__(self):
		self.game = []

	def append(self, fenCode):
		self.game.append(fenCode)

	def commit(self, Username, Name, Mode):
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO tblGames (Username, Name, Game, Mode)
			VALUES (?,?,?,?)""", (Username, Name, json.dumps(self.game), Mode))
		conn.commit()

	def listAll(self, Username):
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""SELECT Name, Mode
			FROM tblGames
			WHERE Username = '%s'""" % Username)
		contents = cursor.fetchall()
		return contents

	def read(self, GameID):
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""SELECT Game
			FROM tblGames
			WHERE GameID = '%s'""" % GameID)
		contents = cursor.fetchone()
		print(contents)
		return json.loads(contents[0])