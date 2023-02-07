#!/usr/bin/env python3

import asyncio, os

from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import telegram

html_page = urlopen(Request('https://developer.android.com/jetpack/androidx/releases/compose-kotlin')).read()

soup = BeautifulSoup(html_page, 'html.parser')
latest_compose_compiler, kotlin_compatibility = [x.text for x in soup.select_one('main table tbody tr').select('td')]

with open('compose-version', 'r') as f: latest_notified_compose = f.read()
if latest_notified_compose != latest_compose_compiler:
    with open('compose-version', 'w') as f: f.write(latest_compose_compiler)
    text = f'Latest version of Compose Compiler, <code>{latest_compose_compiler}</code>, has been ' \
           f'released which is compatible with Kotlin <code>{kotlin_compatibility}</code>.'
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    asyncio.run(bot.send_message(chat_id='@Persian_Calendar', text=text, parse_mode='HTML'))
