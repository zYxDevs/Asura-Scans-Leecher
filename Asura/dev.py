from Asura.db_funcs import get_served_chats, add_dev
from Asura import DEVS, asura, get_command, BOT_NAME, BOT_USERNAME, API_ID, API_HASH, TOKEN, MONGO_URI, PREFIXES 
import os
from pyrogram import filters
import asyncio




@asura.on_message(get_command("broadcast") & filters.user(DEVS))
async def _broadcast(_, message):
  chats = await get_served_chats()
  sent = 0
  await message.reply_text(f"**Starting Broadcast**\n\n**ETA**: `{len(chats)*2} seconds`")
  if message.reply_to_message:
    for chat in chats:
      try:
        await message.reply_to_message.copy(chat)
      except:
        pass
      await asyncio.sleep(1)
      sent += 1
  else:
    for chat in chats:
      try:
        await asura.send_message(chat_id=chat, text=message.text.split(" ", maxsplit=1)[1])
      except:
        pass
      await asyncio.sleep(1)
      sent += 1
  return await message.reply_text(f"Successfully Broadcasted to `{sent}` chats")



@asura.on_message(get_command("config") & filters.user(DEVS))
async def _config(_, message):
  tex = f"**Configuration of {BOT_NAME}**\n\n"
  tex += f"**COMMAND PREFIXES**: `{' ,'.join(PREFIXES)}`\n"
  tex += f"**SUDO USERS**: `{' ,'.join(DEVS)}`\n"
  tex += f"**API ID**: `{API_ID}`\n"
  tex += f"**API HASH**: `{API_HASH}`\n"
  tex += f"**BOT TOKEN**: `{TOKEN}`\n"
  tex += f"**MONGO URI**: `{MONGO_URI}`\n"
  return await message.reply_text(tex)



@asura.on_message(get_command("addsudo") & filters.user(DEVS))
async def _addsudo(_, message):
  if message.reply_to_message:
    return await add_dev(messages.reply_to_message.from_user.id)
  else:
    try:
      user = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
      return await message.reply_text("Give A Fucking Username or user id nigga")
    if isinstance(user, int):
      return await add_dev(user)
    else:
      user = await asura.get_users(user.replace("@", ""))
      return await add_dev(user.id)
