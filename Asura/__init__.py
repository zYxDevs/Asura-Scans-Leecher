from pyrogram import Client, filters
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
TOKEN = getenv("TOKEN")
MONGO_URI = getenv("MONGO_URI")
PREFIXES = ['!', '/', '.']



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



def get_command(com):
  return filters.command([com, f"{com}@{BOT_USERNAME}"], prefixes=PREFIXES)
