# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from bot import StartTime

startText = "https://telegra.ph/file/d0d0a7f81665ff884a59b.jpg""
Bot by:- @LeviAckerman1709.
Credit:- @LexicaAPI.
Commands:
/draw: create images
/upscale: upscale your images
/gpt: chatgpt
/bard: bard ai by google
/mistral: mistral ai
/llama: llama by meta ai
/palm: palm by google
/reverse: reverse image search
/gemini: gemini by google
"""

@Client.on_message(filters.command(["start","help","repo","source"]))
async def start(_: Client, m: t.Message):
    await = m.reply_photo(
        photo = “” , 
        caption = startText,
        reply_markup=t.InlineKeyboardMarkup(
            [
                [
                    t.InlineKeyboardButton(text="Source",url="https://github.com/Qewertyy/SDWaifuRobot")
                ]
            ]
        )
    )