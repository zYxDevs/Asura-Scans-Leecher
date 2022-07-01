import cloudscraper as c
from bs4 import BeautifulSoup as bs
import os 
import glob
import img2pdf
import requests 
#import asyncio
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Asura import asura, BOT_NAME, BOT_USERNAME, get_command


#loop = asyncio.get_event_loop()


C = "<b> Asura Scans Updates</b> \n\n"
CS = "ヘ <b>Name :</b> <code>{}</code>\n\n"

CHS = "  ヘ [{}]({})\n"

RST = "<b>Name</b>: <code>{}</code>"
RSCH = "» [{}]({})"

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
async def _manga(_, message):
  try:
    url = message.text.split(" ", maxsplit=1)[1]
  except IndexError:
    return await message.reply_text("**Usage **:\n× `/manga` url")
  m = await message.reply_text("**🔍Searching ……**")
  if "asurascans.com" in url:
    file = await _asura(url)
  elif "reaperscans.com" in url:
    file = _reaper(url)
  elif "realmscans.com" in url:
    file = _realm(url)
  else:
    return await m.edit_text("Give a url from realmscans.com | reaperscans.com | asurascans.com")
  await m.edit("⚡Uploading Please Wait …")
  await message.reply_document(file, caption=file[:-4])
  return os.remove(file)


async def _asura(url)
  s = c.create_scraper()
  html = s.get(url).text
  soup = bs(html, 'html.parser')
  title = soup.find_all("title")[0]
  title = title.text.replace(" - Asura Scans", "as.pdf")
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
  pd = pf[:-6] + ".pdf"
  os.rename(pf, pd)
  return pd


@asura.on_message(get_command("start"))
async def _start(_, message):
  await message.reply_text(
    text=f"Hi, I am {BOT_NAME}\nI can help you in getting mangas from [Asura Scans](https://asurascans.com) & [Reaper Scans](https://reaperscans.com) and latest updates from [Asura Scans](https://asurascans.com) & [Reaper Scans](https://reaperscans.com)\n\nTo Know About My Commands Click `HELP` button\nTo know about me Click `ABOUT` button",
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
    text="Following Are My Commands\n\n× /latest  -> Get latest Updates From [Asura Scans](https://asurascans.com)\n× /manga url -> Get pdf of manga chapter by url (Asura scans)\n× /rlatest -> Get latest updates from [Reaper Scans](https://reaperscans.com)\n× /rmanga -> Get pdf of manga chapter by url ( Reaper Scans)",
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="Back",
            callback_data="bback"
          )
        ]
      ]
    ),
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
          ),
          InlineKeyboardButton(
            text="Back",
            callback_data="bback"
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



@asura.on_callback_query(filters.regex("bback"))
async def _bvack(_, query):
  qm = query.message
  return await qm.edit_text(
      text=f"Hi, I am {BOT_NAME}\nI can help you in getting mangas from [Asura Scans](https://asurascans.com) & [Reaper Scans](https://reaperscans.com) and latest updates from [Asura Scans](https://asurascans.com) & [ReaperScans](https://reaperscans.com)\n\nTo Know About My Commands Click `HELP` button\nTo know about me Click `ABOUT` button",
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
   

@asura.on_message(get_command("rlatest"))
async def _rlatest(_, message):
  s = c.create_scraper()
  soup = bs(s.get("https://reaperscans.com").text, 'html.parser')
  tits = soup.find_all("div", attrs={"class":"series-box"})
    
  
    
  titles = []
  for tit in tits:
    title = tit.a.get("href").split("/")[-2]
    title = " ".join(x.capitalize() for x in title.split("-"))
    titles.append(RST.format(title))
    
  chs = []
  chaps = soup.find_all("div", attrs={"class":"series-content"})
  for chap in chaps:
    chap = chap.find_all("a")
    chs2 = []
    for cha in chap:
      ck = cha.get("href")[:-1].split("/")[-1]
      ck = ck.split("-")
      if len(ck) == 3:
        ck = ck[0] + " "+ ck[1] + "." + ck[2]
      else:
        ck = " ".join(ck)
      chs2.append(RSCH.format(ck.capitalize(), cha.get("href")))
    chs.append(chs2)
    
  msg = ""
  for title in titles[:16]:
    st = ""
    st += "× " + title
    st += "\n  " + "\n  ".join(chap for chap in chs[titles.index(title)])
    if "#" in st:
      pass
    else:
      msg += st + "\n\n"
    
  return await message.reply_text(text=msg[:4096], disable_web_page_preview=True)


async def _reaper(url)
  s = c.create_scraper()
  soup = bs(s.get(url).text, 'html.parser')
  title = soup.title
  title= title.string + ".pdf"
  title = title.replace("-"," ")
  images = soup.find_all("img")
  cont = []
  for image in images:
    if (image.get("id")):
      url = image.get("data-src")
      cont.append(url.replace("\t", "").replace("\n", ""))
    else:
      pass
  im = []
  num = 0
  for x in cont:
    content = requests.get(x).content
    open(f'{title[:-4]}-{num}.jpg', 'wb').write(content)
    im.append(f'{title[:-4]}-{num}.jpg')
    num += 1
  titl = title.replace("Reaper Scans", "")
  pf = await pdf(title)
  os.rename(pf, titl)
  return titl


async def _realm(url):
  s = c.create_scraper()
  soup = bs(s.get(url).text, 'html.parser')
  images = soup.find_all("script")
  title = soup.title.text.replace("-", "_") + ".pdf"
  for x in images[25]:
    x = x.split("(",1)[1]
    x = x[:-2]
    resp = loads(x)
  res = (resp['sources'][0]['images'])
  im = []
  num = 0
  for x in res:
    content = requests.get(x).content
    open(f'{title[:-4]}-{num}.jpg', 'wb').write(content)
    im.append(f'{title[:-4]}-{num}.jpg')
    num += 1
  titl = title.replace("_", "")
  titl = titl.replace(" Realm Scans", "")
  pf = await pdf(title)
  os.rename(pf, titl)
  return titl


if __name__ == "__main__":
  #loop.run_until_complete(start_bot())
  idle()
