#!/usr/bin/env python3

import time
import random
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import telegram
import asyncio

async def main():
    page = BeautifulSoup(urlopen(Request('https://www.unicode.org/L2/L-curdoc.htm')), 'html.parser')

    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])

    with open('new-unicode-proposals', 'r') as f: last_id = f.read()

    for row in page.select('.contents table.subtle tr'):
        tds = row.select('td')
        if not tds: continue
        link = tds[0].select_one('a')
        if not link: continue
        row_id = tds[0].text
        if last_id >= row_id: continue
        url = 'https://www.unicode.org/L2/' + link.attrs['href']
        text = f'''<a href="{url}">{tds[0].text}</a>

{tds[1].text}

Source: {tds[2].text}
{tds[3].text}

@unicodeproposals'''
        await bot.send_message(chat_id='@unicodeproposals', parse_mode='HTML', text=text)
        with open('new-unicode-proposals', 'w') as f: f.write(row_id)
        asyncio.sleep(random.uniform(1, 10))

asyncio.run(main())
