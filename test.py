import asyncio
from tkinter import *

class asyncTk(Tk):
	def __init__(self):
		super().__init__()
		self.running = True
		self.protocol("WM_DELETE_WINDOW", self.on_closing)

	def on_closing(self):
		self.running = False
		self.destroy()
		
	def __await__(self):
		while self.running:
			self.update()
			yield

async def asd():
	for x in range(1,10):
		await asyncio.sleep(1)
		print(x)

async def main():
	w = asyncTk()
	asyncio.create_task(asd())
	await w

asyncio.run(main())