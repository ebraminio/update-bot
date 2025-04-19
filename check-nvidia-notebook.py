#!/usr/bin/env python3

import asyncio, os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import unquote
import json

import telegram

page = urlopen(Request('https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/AjaxDriverService.php?func=DriverManualLookup&psid=133&pfid=1073&osID=57&languageCode=1033&beta=null&isWHQL=0&dltype=-1&dch=1&upCRD=null&qnf=0&sort1=1&numberOfResults=10'))
info = json.loads(page.read().decode('utf-8'))['IDS'][0]['downloadInfo']
version = info['Version']

with open('new-nvidia-notebook', 'r') as f: latest_post = f.read()
if version != latest_post:
    with open('new-nvidia-notebook', 'w') as f: f.write(version)
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])

    link = info['DownloadURL']
    page_url = info['DetailsURL']
    size = info['DownloadURLFileSize']
    release_notes = unquote(info['ReleaseNotes']).replace('<br />', '\n')
    comment = BeautifulSoup(release_notes, 'html.parser').text
    text = f'''Driver {version} is out!

Driver Details: {page_url}
Download Driver ({size}): {link}

```
{comment}
```'''
    asyncio.run(bot.send_message(chat_id='@NVIDIANotebookDriver', text=text, parse_mode='markdown', disable_web_page_preview=True))
