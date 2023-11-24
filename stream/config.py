import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    API_ID = os.getenv("API_ID",'')
    API_HASH = os.getenv("API_HASH",'')
    SESSION_STRING = os.getenv("SESSION_STRING",'')