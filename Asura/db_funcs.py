from Asura import db
from typing import Dict, List, Union


chatsdb = db.chats
devsdb = db.devs



async def is_served_chat(chat_id: int) -> bool:
  chat = await chatsdb.find_one({"chat_id": chat_id})
  if not chat:
    return False
  return True


async def get_served_chats() -> list:
  chats_list = []
  async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
    chats_list.append(chat)
  return chats_list


async def add_served_chat(chat_id: int):
  is_served = await is_served_chat(chat_id)
  if is_served:
    return
  return await chatsdb.insert_one({"chat_id": chat_id})



async def get_devs() -> list:
  devs_list = []
  async for dev in devsdb.find({"dev_id": {"$gt": 0}}):
    devs_list.append(dev)
  return devs_list


async def add_dev(dev_id: int):
  devs = await get_devs()
  if dev_id in devs:
    return
  return await devsdb.insert_one({"dev_id": dev_id})


async def rm_dev(dev_id: int):
  devs = await get_devs()
  if dev_id in devs:
    return await devsdb.delete_one({"dev_id": dev_id})
  return
