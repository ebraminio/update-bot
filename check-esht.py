#!/usr/bin/env python3

import asyncio, os

from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import telegram

html_page = urlopen(Request('http://esht.ir')).read()

soup = BeautifulSoup(html_page, 'html.parser')
img = soup.select_one('input[type="image"]')['src']

with open('new-esht', 'r') as f: latest_post = f.read()
if latest_post != img:
    with open('new-esht', 'w') as f: f.write(img)
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    img_bytes = urlopen(Request('http://esht.ir/' + img)).read()
    asyncio.run(bot.send_photo(chat_id='@fruitprices', photo=img_bytes))
