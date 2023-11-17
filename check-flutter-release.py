#!/usr/bin/env python3

import asyncio, os
import json
from urllib.request import Request, urlopen

import telegram

content = json.loads(urlopen(Request('https://storage.googleapis.com/flutter_infra_release/releases/releases_linux.json')).read())

latest_version_hash = content['current_release']['stable']
latest_version = [x for x in content['releases'] if x['hash'] == latest_version_hash][0]['version']

with open('new-flutter-release', 'r') as f: latest_notified_version = f.read()
if latest_notified_version != latest_version:
    with open('new-flutter-release', 'w') as f: f.write(latest_version)
    text = f"A new stable version of Flutter, {latest_version}, is published.\n\nhttps://docs.flutter.dev/get-started/install"
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    asyncio.run(bot.send_message(chat_id='@FlutterNewsFeed', text=text, parse_mode='HTML'))
