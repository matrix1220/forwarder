from pyrogram import Client, idle

api_id = 123
api_hash = "123"

usernames_list = ["@someuser","@aother"]

with Client("account", api_id, api_hash) as app:
	@app.on_message()
	def my_handler(client, message):
		print(message)

	idle()