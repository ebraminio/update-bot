#!/usr/bin/env python3

import os, asyncio
from datetime import datetime
import zoneinfo

import telegram

from persiancalendar import persian_from_fixed, fixed_from_gregorian

with open('new-time', 'r') as f: latest_post = f.read()

async def main():
    tehran_tz = zoneinfo.ZoneInfo("Asia/Tehran")
    time = datetime.now(tehran_tz)

    persian = persian_from_fixed(fixed_from_gregorian((time.year, time.month, time.day)))
    text = '`' + '/'.join(map(str, persian)) + '`\n\n`' + time.date().isoformat() + '`'

    if text != latest_post:
        with open('new-time', 'w') as f: f.write(text)
        
        bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
        await bot.send_message(chat_id='@ebraminio', parse_mode='markdown', text=text)

asyncio.run(main())
