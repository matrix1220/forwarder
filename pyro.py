from pyrogram import Client
from pyrogram.handlers import MessageHandler

api_id = 123
api_hash = "123"

# def my_function(client, message):
#     print(message)


# app = Client("account", api_id, api_hash, test_mode=True)

# app.add_handler(MessageHandler(my_function))

# app.run()


with Client("account", api_id, api_hash) as app:
	async def main():
		print(len([x async for x in app.iter_dialogs()]))

	app.run(main())