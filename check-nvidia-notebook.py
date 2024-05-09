#!/usr/bin/env python3

import asyncio, os
from urllib.request import Request, urlopen
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

import telegram

page_url_stub = urlopen(Request('https://www.nvidia.com/download/processDriver.aspx?psid=129&pfid=1004&rpf=1&osid=135&lid=1&lang=en-us&ctk=0&dtid=1&dtcid=1')).read()
page_url = 'https://www.nvidia.com/download/' + page_url_stub.decode()
page_content = urlopen(Request(page_url)).read()

soup = BeautifulSoup(page_content, 'html.parser')

link = 'https://us.download.nvidia.com' + parse_qs(urlparse(soup.select_one('#lnkDwnldBtn')['href']).query)['url'][0]
version = soup.select_one('#tdVersion').text.split('WHQL')[0].strip()

with open('new-nvidia-notebook', 'r') as f: latest_post = f.read()
if version != latest_post:
    with open('new-nvidia-notebook', 'w') as f: f.write(version)
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    comment = soup.select_one('#tab1_content').text.split(' updates for your notebook.')[1].split('Learn more in our Game Ready Driver article here.')[0].strip()
    size = [x for x in soup.select('.contentsummaryright') if ' MB' in x.text][0].text.strip()
    text = f'''Driver {version} is out!

Driver Details: {page_url}
Download Driver ({size}): {link}

```
{comment}
```'''
    asyncio.run(bot.send_message(chat_id='@NVIDIANotebookDriver', text=text, parse_mode='markdown', disable_web_page_preview=True))
