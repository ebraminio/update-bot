#!/usr/bin/env python3

import asyncio, os

from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
import cssutils
import telegram

html_page = urlopen(Request('https://eitaa.com/barforooshan')).read()

soup = BeautifulSoup(html_page, 'html.parser')
latest_post_element = [x for x in soup.select('.etme_widget_message_bubble') if '#نرخ_قیمت' in x.text][-1].select_one('.etme_widget_message_photo_wrap')
latest_post = latest_post_element['href']
img = 'https://eitaa.com/' + cssutils.parseStyle(latest_post_element['style'])['background-image'].replace('url(', '').replace(')', '')

with open('new-esht', 'r') as f: latest_posted = f.read()
if latest_posted != latest_post:
    with open('new-esht', 'w') as f: f.write(latest_post)
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    img_bytes = urlopen(Request(img)).read()
    asyncio.run(bot.send_photo(chat_id='@fruitprices', photo=img_bytes))
