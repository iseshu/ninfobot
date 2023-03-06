import os
import time
import requests
from tinydb import TinyDB, Query
from requests.structures import CaseInsensitiveDict
from pyrogram import filters, Client,enums
from pyrogram.types.messages_and_media import message
from pyrogram.types import *
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)
db = TinyDB('data.json')
User = Query()
API_ID = os.environ.get('API_ID')
BASE_URL = os.environ.get('BASE_URL')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
NEXT_OFFSET = 25
CACHE_TIME = 0

bot = Client('bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('info') & filters.private)
async def start(bot, message):
    text = message.text
    if text == "/info":
        await bot.send_message(message.chat.id,text = "Use this format to get student information : **/info <adminnumber>**\n Copy `/info `")
    else:
        i_d = text.replace("/info ","")
        if len(i_d) == 7:
            msg = await bot.send_message(message.chat.id, "🔎 Getting `{}` Information ".format(i_d))
            dat = db.search(User.id_no == str(i_d))
            if len(dat) == 1:
                data = dat[0]
            else:
                req = requests.get(f"{BASE_URL}/get?id="+i_d)
                data = req.json()
                if data["status"] == True:
                    db.insert(data)
            if data["status"] == True:
                text = f"|--**Here The Details Of {i_d}**--\n|->🙍**Name**: `{data['name']}`\n|->🧍**Father Name**: `{data['father_name']}`\n|->🔢**Admin No**: `{data['id_no']}`\n|->🧑‍🏫**Class**: `{data['class_n']}`\n|->🏦**Branch**: `{data['branch']}`\n|->💰**Due Amount**: `{data['due_amount']}`\n|->☎️**Mobile Number**: || {data['mobile']} ||\n|(Created By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/))"
                await msg.delete()
                await bot.send_message(message.chat.id, text, protect_content=False,parse_mode=enums.ParseMode.MARKDOWN,
                                        reply_markup=InlineKeyboardMarkup(
                                            [
                                                [
                                                    InlineKeyboardButton(
                                                        "Support 💖", url="https://t.me/yssprojects"),
                                                    InlineKeyboardButton(
                                                        "Developer 🙍", url="https://t.me/seshu2004")
                                                ]
                                            ]
                                        )
                                        )

            else:
                await msg.edit_text("I'm Sorry, I Can't Find Your Information \nPlease Try Again Using /info Command\n/help For More Details")
        else:
            await bot.send_message(message.chat.id, "Please Enter A Valid I'd")


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await bot.send_message(message.chat.id,
                           reply_to_message_id=message.id,
                           text=f"Hello **{message.chat.first_name}!**\nI'm **Narayana Sudent Information Spoiler Bot**\nI'll Get Information of Naryana Students Using Admission Number\nTo Get Information Use /info\nFor More Use /help\nI'm Created By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)",
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                       InlineKeyboardButton(
                                           "Support 💖", url="https://t.me/yssprojects"),
                                       InlineKeyboardButton(
                                           "Developer 🙍", url="https://t.me/seshu2004")
                                   ]
                               ]
                           )
                           )


@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await bot.send_message(message.chat.id,
                           reply_to_message_id=message.id,
                           text=f"Hello **{message.chat.first_name}!**\nI'll Get Information of Naryana Students Using Admission Number\nTo Get Information Use /info\n Your Admission Number Must Me 7 Digits And Number\nI'm Created By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/)",
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                       InlineKeyboardButton(
                                           "Support 💖", url="https://t.me/yssprojects"),
                                       InlineKeyboardButton(
                                           "Developer 🙍", url="https://t.me/seshu2004")
                                   ]
                               ]
                           )
                           )

@bot.on_message(filters.command('admin') & filters.private)
async def start(bot, message):
    data = db.all()
    await bot.send_message(message.chat.id,reply_to_message_id=message.id,text=f"**Hello Admin** \nTotal Users🙍 : `{len(data)}`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Refresh 🔄", callback_data="refreshdata"),InlineKeyboardButton("Get Data 📁", callback_data="getdatafile")]]))

@bot.on_callback_query()
async def callback(client, query_callback):
    msg = query_callback.data
    if msg == "refreshdata":
        data = db.all()
        await query_callback.message.edit_text(text=f"**Hello Admin** \nTotal Users🙍 : `{len(data)}`\nTimestamp : `{time.time()}`",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Refresh 🔄", callback_data="refreshdata"),InlineKeyboardButton("Get Data 📁", callback_data="getdatafile")]]))
    elif msg == "getdatafile":
        await bot.send_document(query_callback.from_user.id,"data.json")

if __name__ == "__main__":
    bot.run()
