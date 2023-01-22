#!/usr/bin/env python3
import asyncio, re, os
from urllib.request import Request, urlopen
from urllib.parse import quote

import telegram
from bs4 import BeautifulSoup

html_page = urlopen(Request('https://www.newyorker.com/cartoons/daily-cartoon')).read()

soup = BeautifulSoup(html_page, 'html.parser')
post = soup.find('main').find('main').find('ul').find_all('li')[0]
img_url = re.sub(r'/[\d:]+/[^/]+', '', post.find('img')['src'])
caption = '\n\n'.join(x.text for x in post.select('h3, h4, h5'))
url = 'https://www.newyorker.com/' + quote(post.find('a')['href'].lstrip('/'))

latest_post = open('new-yorker-latest-post', 'r').read()
if latest_post != caption:
    with open('new-yorker-latest-post', 'w') as f: f.write(caption)
    author = post.find('p').text
    msg = caption + f'\n\n<a href="{url}">{author}</a>\n\n@new_yorker_cartoons'
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    asyncio.run(bot.send_photo(chat_id='@new_yorker_cartoons', photo=img_url, parse_mode='HTML', caption=msg))
