from pyrogram import Client
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
TOKEN = getenv("TOKEN")
LOG = getenv("LOG")

asura = Client(
  "ASURA",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=TOKEN
)
print("[INFO]: STARTING BOT")
asura.start()

print("[INFO]: GATHERING INFO")
x = asura.get_me()
BOT_NAME = x.first_name
BOT_USERNAME = x.username
BOT_ID = x.id
