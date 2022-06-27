import cloudscraper as c
from bs4 import BeautifulSoup as bs
import os 
import glob
import img2pdf
import requests 
#import asyncio
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Asura import asura, BOT_NAME, BOT_USERNAME, LOG


#loop = asyncio.get_event_loop()


C = "<b> Asura Scans Updates</b> \n\n"
CS = "ヘ <b>Name :</b> <code>{}</code>\n\n"

CHS = "  ヘ [{}]({})\n"
"""
async def start_bot():
  return await asura.send_message(chat_id=LOG, text='Im Alive')
"""


def get_command(com):
  return filters.command([com, f"{com}@{BOT_USERNAME}"], prefixes=['!', '/', '.'])


async def sorted():
  def ssh(a):
    return int(a.split("-",1)[1].split('.')[0])
  
  f = glob.glob("./*jpg")
  f.sort(key=ssh)
  return f


async def pdf(name):
  lis = await sorted()
  for im in lis:
    if not name[:-4] in im:
      lis.remove(im)
    else:
      pass
  with open(name, 'wb') as f:
    f.write(img2pdf.convert(lis))
    f.close()
  for a in lis:
    os.remove(a)
  return name




@asura.on_message(get_command("manga"))
async def _asura(_, message):
  try:
    url = message.text.split(" ", maxsplit=1)[1]
  except IndexError:
    return await message.reply_text("**Usage **:\n× `/manga` url")
  m = await message.reply_text("**🔍Searching ……**")
  s = c.create_scraper()
  html = s.get(url).text
  soup = bs(html, 'html.parser')
  title = soup.find_all("title")[0]
  title = title.text.replace(" - Asura Scans", ".pdf")
  title = title.replace("-", "_")
  ims = soup.find_all("img", attrs={'loading':'lazy'})
  cont = ""
  num = 0
  flist = []
  for im in ims:
    if "wp-post-image" in im.get("class"):
      ims.remove(im)
    else:
      if im.get("src"):
        d = requests.get(im.get("src")).content
        open(f"{title[:-4]}-{num}.jpg", "wb").write(d)
      else:
        pass
      num += 1
  pf = await pdf(title)
  await m.edit_text("⚡Uploading Please Wait …")
  await message.reply_document(pf)
  await m.delete()
  return os.remove(pf)


@asura.on_message(get_command("start"))
async def _start(_, message):
  await message.reply_text(
    text=f"Hi, I am {BOT_NAME}\nI can help you in getting mangas from [Asura Scans](https://asurascans.com) and latest updates from [Asura Scans](https://asurascans.com)\n\nTo Know About My Commands Click `HELP` button and to know about my developer Click `ABOUT` button",
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="HELP",
            callback_data="hhelp"
          ),
          InlineKeyboardButton(
            text="ABOUT",
            callback_data="abbout"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )
  return 

@asura.on_callback_query(filters.regex("hhelp"))
async def hhelp(_, query):
  qm = query.message
  return await qm.edit_text(
    text="Following Are My Commands\n\n×`/latest` -> Get latest Updates From [Asura Scans](https://asurascans.com)\n× `/manga <url>` -> Get pdf of manga chapter by url",
    disable_web_page_preview=True
  )


@asura.on_callback_query(filters.regex("abbout"))
async def abblp(_, query):
  qm = query.message
  return await qm.edit_text(
    text=f"Hey There,\nI am {BOT_NAME}\nMade with ❤️ by @TechZBots\nBelow Are Some Useful Links", 
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="Support",
            url="t.me/Techzbots_support"
          ),
          InlineKeyboardButton(
            text="Updates",
            url="t.me/TechZBots"
          )
        ],
        [
          InlineKeyboardButton(
            text="DEV",
            user_id=5365575465
          ),
          InlineKeyboardButton(
            text="Manga Channel",
            url="t.me/The_Manga_Hub"
          )
        ],
        [
          InlineKeyboardButton(
            text="Repo",
            url="https://github.com/AuraMoon55/Asura-Scans-Leecher"
          )
        ]
      ]
    )
  )



@asura.on_message(get_command("latest"))
async def latest(_, message):
  s = c.create_scraper()
  a = s.get("https://asurascans.com").content
  sp = bs(a, 'html.parser')
  divs = sp.find_all("div", attrs={"class":"luf"})
  res = []
  for x in divs:
    title = x.h4.string
    msg = CS.format(title)
    for li in x.ul:
      msg += CHS.format(li.a.string, li.a.get("href"))
    res.append(msg)
  lim = int(4096/len(res[0])) + 1
  C = ""
  for x in res[:lim]:
    C += x
    C += "\n"
  return await message.reply(C, disable_web_page_preview=True)



if __name__ == "__main__":
  #loop.run_until_complete(start_bot())
  idle()
