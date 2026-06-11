#!/usr/bin/env python3

import os, asyncio, json, zoneinfo
from datetime import datetime

import telegram

from persiancalendar import persian_from_fixed, fixed_from_gregorian


translation_table = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
def to_persian_num(number): return str(number).translate(translation_table)

persian_months = {
    1: "فروردین", 2: "اردیبهشت", 3: "خرداد",
    4: "تیر", 5: "مرداد", 6: "شهریور",
    7: "مهر", 8: "آبان", 9: "آذر",
    10: "دی", 11: "بهمن", 12: "اسفند"
}
def format_persian_date(year, month, day):
    p_day = to_persian_num(day)
    month_name = persian_months.get(month, "")
    p_year = to_persian_num(year)
    return f"{p_day} {month_name} {p_year}"

persian_weekdays = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']

with open('new-time', 'r') as f: latest_post = json.loads(f.read())

async def main():
    tehran_tz = zoneinfo.ZoneInfo("Asia/Tehran")
    time = datetime.now(tehran_tz)

    persian = persian_from_fixed(fixed_from_gregorian((time.year, time.month, time.day - 1)))
    text = '`' + '/'.join(map(str, persian)) + '`\n\n`' + time.date().isoformat() + '`'
    # print(text)

    if text != latest_post['text']:
        bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
        persian_day = persian_weekdays[time.weekday()]

        await bot.edit_message_text(chat_id='@ebraminio', parse_mode='markdown', message_id=42, text=text)

        await bot.set_chat_title(chat_id='@ebraminio', title=persian_day + '، ' + format_persian_date(*persian))
        title_change_id = latest_post['id']
        try:
            await bot.delete_message(chat_id='@ebraminio', message_id=title_change_id)
        except telegram.error.BadRequest:
            pass

        with open('new-time', 'w') as f: f.write(json.dumps({'text': text, 'id': title_change_id + 1}))

asyncio.run(main())
