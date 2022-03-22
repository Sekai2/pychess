import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import sqlite3
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

		login_button = ttk.Button(root, text='login', command = lambda: login.hashCheck(username, password))
		login_button.pack(ipadx = 5, ipady = 5, expand = True)

		create_account_button = ttk.Button(root, text='Create Account', command = lambda: login.create(username, password))
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
		hashed = passwordHash(password)
		conn = sqlite3.connect('chessplayers.db')
		cursor = sqlite3.cursor()
		sql = "INSERT INTO username"

	def hashCheck(username, password):
		hashed = passwordHash(password)
		conn = sqlite3.connect('chessplayers.db')

login.menu()