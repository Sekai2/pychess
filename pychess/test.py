import sqlite3
mydb = sqlite3.connect('chessplayers.db')
cursor = mydb.cursor()
cursor.execute("""SELECT * FROM tblUsers""")
a = cursor.fetchall()
print(a)