#!/usr/bin/env python3

import asyncio, os
from xml.etree import ElementTree

from urllib.request import Request, urlopen

import telegram

content = urlopen(Request('https://dl.google.com/android/maven2/com/android/application/group-index.xml')).read()
agp_versions = ElementTree.fromstring(content).find('com.android.application.gradle.plugin').get('versions').split(',')

latest_agp = [x
              for x in agp_versions
              if '-alpha' not in x
              if '-beta' not in x
              if '-rc' not in x][-1]

with open('agp-version', 'r') as f: latest_notified_agp = f.read()
if latest_notified_agp != latest_agp:
    with open('agp-version', 'w') as f: f.write(latest_agp)
    text = f"A new version of stable Android Studio, <code>{latest_agp}</code>, has been released. An update to" \
            " <code>com.android.application</code> (AGP) as well as Android Studio's installation might be needed."
    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    asyncio.run(bot.send_message(chat_id='@Persian_Calendar', text=text, parse_mode='HTML'))
