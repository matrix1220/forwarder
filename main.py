from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler
from pyrogram.errors import SessionPasswordNeeded, BadRequest
from pyrogram.types import Chat, ChatPreview

from tkinter import *
import asyncio

import tkinter.messagebox
import _thread
import os.path

api_id = 123
api_hash = "123"

title = "Frowarder"

#loop = asyncio.get_event_loop()


class asyncTk(Tk):
	def __init__(self):
		super().__init__()
		self.running = True
		self.yield_from = None
		self.protocol("WM_DELETE_WINDOW", self.on_closing)

	def on_closing(self):
		self.running = False
		self.destroy()
		
	def __await__(self):
		while self.running:
			self.update()
			yield
		else:
			if not self.yield_from == None:
				yield from self.yield_from

	__iter__ = __await__

def async_call(coro):
	def temp():
		asyncio.create_task(coro())
	return temp

def showerror(err, root):
	top = Toplevel(root)

	label = Label(top, text = err)
	label.pack(side = TOP)

	button = Button(top, text = "OK", command = top.destroy)
	button.pack(side = BOTTOM)

class ask(asyncTk):
	def __init__(self, qusetion):
		super().__init__()
		self.geometry("400x400")

		self.frame = Frame(self)
		self.frame.pack(expand=True)

		label = Label(self.frame, text = qusetion)
		label.pack(side = TOP)

		self.entry = Entry(self.frame, bd = 5)
		self.entry.pack(side = TOP)

		button = Button(self.frame, text = "OK", command = async_call(self.ok))
		button.pack(side = BOTTOM)

	async def ok(self):
		self.on_closing()

class askPhone(ask):
	def __init__(self, tgclient):
		super().__init__("what is your phone number?")
		self.tgclient = tgclient

	async def ok(self):
		try:
			phone = self.entry.get()
			sentcode = await self.tgclient.send_code(phone)
			self.yield_from = askCode(self.tgclient, sentcode, phone)
			self.on_closing()
		except BadRequest as e:
			showerror(str(e), self)

class askCode(ask):
	def __init__(self, tgclient, sentcode, phone):
		super().__init__("code?")
		self.tgclient = tgclient
		self.sentcode = sentcode
		self.phone = phone

		label = Label(self.frame, text = "Code sent via " + sentcode.type)
		label.pack(side = TOP)

		self.button = Button(self.frame, text = "resend", state=DISABLED, command = async_call(self.resend))
		self.button.pack(side = BOTTOM)
		asyncio.create_task(self.resendwait())

	async def resendwait(self):
		if self.sentcode.timeout:
			while self.sentcode.timeout > 0 and self.running:
				self.button['text'] = "resend after " + str(self.sentcode.timeout)
				await asyncio.sleep(1)
				self.sentcode.timeout = self.sentcode.timeout - 1
		if self.running:
			self.button['text'] = 'resend'
			self.button['state'] = 'normal'

	async def resend(self):
		sentcode = await self.tgclient.resend_code(self.phone, self.sentcode.phone_code_hash)
		self.yield_from = askCode(self.tgclient, sentcode, self.phone)
		self.on_closing()

	async def ok(self):
		try:
			code = self.entry.get()
			await self.tgclient.sign_in(self.phone, self.sentcode.phone_code_hash, code)
			self.on_closing()
		except BadRequest as e:
			showerror(str(e), self)
		except SessionPasswordNeeded as e:
			self.yield_from = askPassword(self.tgclient)
			self.on_closing()

class askPassword(ask):
	def __init__(self, tgclient):
		super().__init__("password?")
		self.tgclient = tgclient

	async def ok(self):
		try:
			await self.tgclient.check_password(self.entry.get())
			self.on_closing()
		except BadRequest as e:
			showerror(str(e), self)
	


class Forward:
	def __init__(self, from_chat, to_chat):
		self.from_chat = from_chat
		self.to_chat = to_chat

	def handle(self, client, message):
		if message.chat.id == self.from_chat:
			client.forward_messages(self.to_chat, message.chat.id, [message.message_id])

class Hndlr(Toplevel):
	def __init__(self, root):
		super().__init__(root)
		self.geometry("200x200")
		self.root = root
		self.l1 = Label(self, text='source channel:')
		self.l1.pack(side = TOP, fill = X, padx=20)
		self.e1 = Entry(self)
		self.e1.pack(side = TOP, fill = X, padx=20)

		self.l2 = Label(self, text='destination:')
		self.l2.pack(side = TOP, fill = X, padx=20)
		self.e2 = Entry(self)
		self.e2.pack(side = TOP, fill = X, padx=20)

		button2 = Button(self, text = "ok", command = async_call(self.ok))
		button2.pack(side = BOTTOM, fill=X)

	async def ok(self):
		self.destroy()


class Hndlrnew(Hndlr):
	def __init__(self, root):
		super().__init__(root)

	async def ok(self): #testchannel_821
		try:
			#print(self.e1.get())
			#chat1 = self.e1.get()
			chat1 = await tgclient.get_chat(self.e1.get())
			if type(chat1)==ChatPreview: chat1 = await tgclient.join_chat(self.e1.get())
			#chat1 = chat1.id

			if self.e2.get()=="me":
				chat2 = self.e2.get()
			else:
				chat2 = await tgclient.get_chat(self.e2.get())
				if type(chat2)==ChatPreview: chat2 = await tgclient.join_chat(self.e2.get())
				chat2 = chat2.id

			self.root.handlers.append(Forward(chat1.id, chat2))
			self.root.listbox.insert(END, chat1.title)
			await super().ok()
		except BadRequest as e:
			showerror(str(e), self)
		

class Main(asyncTk):
	def __init__(self, tgclient):
		super().__init__()
		self.geometry("400x400")
		self.tgclient = tgclient
		self.listbox = Listbox(self)
		self.listbox.pack(side = TOP, fill=BOTH)

		button4 = Button(self, text = "log out", command = async_call(self.log_out))
		button4.pack(side = BOTTOM, fill=X)

		button2 = Button(self, text = "new", command = self.new_handler)
		button2.pack(side = BOTTOM, fill=X)

		button3 = Button(self, text = "delete", command = self.delete_handler)
		button3.pack(side = BOTTOM, fill=X)


		self.handlers = []
		self.mhandler = self.tgclient.add_handler(MessageHandler(self.handler))
		#self.tgclient.remove_handler(*self.mhandler)

	def new_handler(self):
		Hndlrnew(self)

	async def log_out(self):
		await self.tgclient.log_out()
		self.on_closing()

	def delete_handler(self):
		index = self.listbox.curselection()[0]
		del self.handlers[index]
		self.listbox.delete(index)

	def handler(self, client, message):
		print(message)
		for hand in self.handlers:
			hand.handle(client, message)

tgclient = Client("account", api_id, api_hash)

async def main():
	if not await tgclient.connect():
		await askPhone(tgclient)

	await tgclient.initialize()
	await tgclient.get_me()

	await Main(tgclient)

	await tgclient.terminate()
	await tgclient.disconnect()


tgclient.run(main())