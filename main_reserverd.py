import os.path
from pyrogram import Client
from tkinter import *
import tkinter.messagebox

api_id = 123
api_hash = "123"

class LoginPhone:
	def __init__(self):
		self.tgclient = Client(":memory:", api_id, api_hash)
		self.top = Tk()
		Button(self.top, text = "Say Hello", command = self.login)
		L1 = Label(self.top, text="User Name")
		L1.pack( side = LEFT)
		E1 = Entry(self.top, bd =5)
		E1.pack(side = RIGHT)

	def login(self):
		pass

if os.path.isfile("account.session"):
	session = open("account.session").read()
	try:
		tgclient = Client(session)
	except Exception as e:
		tkinter.messagebox.showerror("Frowarder", str(e))
		LoginPhone()
	else:
		pass
else:
	LoginPhone()
