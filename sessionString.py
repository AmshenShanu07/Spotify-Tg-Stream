from pyrogram import Client
import os

api_id = int(input("Enter Api Id:"))
api_hash = input("Enter Api Hash:")

app = Client("my_account", api_id=api_id, api_hash=api_hash)

async def generateToken():
  await app.start()
  token = await app.export_session_string()
  await app.send_message('me', f"`{token}`")
  os.remove('my_account.session')

app.run(generateToken())


