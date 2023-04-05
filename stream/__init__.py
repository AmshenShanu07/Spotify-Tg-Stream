from pyrogram import Client
from stream.config import Config
from pytgcalls import PyTgCalls 


app = Client('my_bot',api_id=Config.API_ID,api_hash=Config.API_HASH,bot_token=Config.BOT_TOKEN)

tgCall = PyTgCalls(app);
