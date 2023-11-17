#!/usr/bin/env python3

import asyncio, os

import feedparser
import telegram

async def main():
    d = feedparser.parse('https://medium.com/feed/flutter')

    with open('new-flutter-blog-posts', 'r') as f: posted_ids = f.read()

    # if the stored file has same feed ids as the remote feed file, bail out
    ids = '\n'.join(e.id for e in d.entries)
    if posted_ids == ids: return

    # save remote feed ids on a file
    with open('new-flutter-blog-posts', 'w') as f: f.write(ids)

    bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
    for entry in reversed(d.entries):
        if entry.id in posted_ids: continue
        text = f"{entry.title}\n\n{entry.link.split('?')[0]}"
        await bot.send_message(chat_id='@FlutterNewsFeed', text=text, parse_mode='HTML')

asyncio.run(main())
