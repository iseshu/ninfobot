import os
import requests
from pyromod import listen
from requests.structures import CaseInsensitiveDict
from pyrogram import filters, Client
from pyrogram.types.messages_and_media import message
from pyrogram.types import *
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

API_ID = os.environ.get('API_ID')
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
    i_d = await bot.ask(
        message.chat.id,
        f"Hello **{message.chat.first_name}!**\n"
        "Send The Narayana Admission Number (NAN) of the student you want to get information about.\n",
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
    id = i_d.text
    if len(id) == 7:
        msg = await bot.send_message(message.chat.id, "🔎 Getting `{}` Information ".format(i_d.text))
        req = requests.get(
            "https://npayapi-in.herokuapp.com/get?id={}".format(id))
        if req.status_code == 200:
            data = req.json()
            if data["status"] == True:
                text = f"|--**Here The Details Of {id}**--\n|->🙍**Name**: `{data['name']}`\n|->🧍**Father Name**: `{data['father_name']}`\n|->🔢**Admin No**: `{data['id_no']}`\n|->🧑‍🏫**Class**: `{data['class_n']}`\n|->🏦**Branch**: `{data['branch']}`\n|->💰**Due Amount**: `{data['due_amount']}`\n|->☎️**Mobile Number**: || `{data['mobile']}` ||\n|(Created By [Seshu Sai](https://www.instagram.com/_yarra.s.s_/))"
                await msg.delete()
                await bot.send_message(message.chat.id, text, reply_to_message_id=i_d.id, protect_content=True,
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

if __name__ == "__main__":
    bot.run()
