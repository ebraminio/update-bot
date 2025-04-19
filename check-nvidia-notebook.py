#!/usr/bin/env python3

import asyncio, os
from urllib.request import Request, urlopen
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

import telegram

page_url = urlopen(Request('https://www.nvidia.com/download/processDriver.aspx?psid=129&pfid=1004&rpf=1&osid=135&lid=1&lang=en-us&ctk=0&dtid=1&dtcid=1')).read().decode('utf-8')
page_content = urlopen(Request(page_url)).read()

soup = BeautifulSoup(page_content, 'html.parser')

#version = soup.select_one('#tdVersion').text.split('WHQL')[0].strip()

with open('new-nvidia-notebook', 'r') as f: latest_post = f.read()
if page_url != latest_post:
    with open('new-nvidia-notebook', 'w') as f: f.write(page_url)
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    # comment = soup.select_one('#tab1_content').text.split(' updates for your notebook.')[1].split('Learn more in our Game Ready Driver article here.')[0].strip()
    # size = [x for x in soup.select('.contentsummaryright') if ' MB' in x.text][0].text.strip()
    text = f'''New driver is out!

Download Driver: {page_url}'''

# ```
# {comment}
# ```'''
    asyncio.run(bot.send_message(chat_id='@NVIDIANotebookDriver', text=text, parse_mode='markdown', disable_web_page_preview=True))
