from pyrogram import Client
from stream.config import Config
from pytgcalls import PyTgCalls


app = Client('my_account', api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.SESSION_STRING)

tgCall = PyTgCalls(app);
