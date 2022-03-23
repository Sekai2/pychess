import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import sqlite3

from PRNG import *
#login system
class login():
	def menu():
		#login screen
		root = tk.Tk()
		window_width = 300
		window_height = 200
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		centre_x = screen_width // 2 - window_width // 2
		centre_y = screen_height // 2 - window_height // 2
		root.geometry(f"{window_width}x{window_height}+{centre_x}+{centre_y}")
		root.resizable(False, False)
		root.attributes("-topmost", 1)

		username = tk.StringVar()
		password = tk.StringVar()

		signin = ttk.Frame(root)
		signin.pack(padx = 10, pady = 10, fill = 'x', expand = True)

		ttk.Label(signin, text = "Username:").pack(fill = "x", expand = True)
		user_entry = ttk.Entry(signin, textvariable = username)
		user_entry.pack(fill = "x", expand = True)
		user_entry.focus()

		ttk.Label(signin, text = "Password:").pack(fill = "x", expand = True)
		pass_entry = ttk.Entry(signin, textvariable = password, show = "*")
		pass_entry.pack(fill = "x", expand = True)

		login_button = ttk.Button(root, text='login', command = lambda: login.hashCheck(str(username.get()), str(password.get())))
		login_button.pack(ipadx = 5, ipady = 5, expand = True)

		create_account_button = ttk.Button(root, text='Create Account', command = lambda: login.create(str(username.get()), str(password.get())))
		create_account_button.pack(ipadx = 5, ipady = 5, expand = True)

		root.mainloop()



	#password hasher
	def passwordHash(password):
		numbers = PRNG.LCG(len(password), 257991014)
		h = 0
		for i in range(len(password)):
			h = h ^ ord(password[i]) ^ numbers[i]
		return h

	def create(username, password):
		wrongLabel = ttk.Label(text='Username already taken', foreground='red')
		hashed = login.passwordHash(password)
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""SELECT Username
			FROM tblUsers
			WHERE Username = '%s'""" % username)
		check = cursor.fetchall()
		print(check)
		if len(check) == 0:
			cursor.execute("""INSERT INTO tblUsers (Username, Hash)
				VALUES (?,?)""", (username, hashed))
			print((username, hashed))
			conn.commit()

		else:
			wrongLabel.pack(fill = 'x', expand = True)

	def hashCheck(username, password):
		hashed = login.passwordHash(password)
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""SELECT Username, Hash
			FROM tblUsers
			WHERE Username = '%s'""" % username)
		details = cursor.fetchall()
		if details[0][1] == hashed:
			return True

		else:
			return False
while __name__ == '__main__':
	login.menu()