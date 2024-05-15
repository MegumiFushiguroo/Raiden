# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from bot import StartTime

startText = ''' 
Bot by:- @LeviAckerman1709.
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
/assis: Ask anything bot will reply in voice format 
'''

Aaru ="https://telegra.ph/file/9567207165204df2503bf.jpg"

@Client.on_message(filters.command(["start","help"]))
async def start(_: Client, m: t.Message):
    await  m.reply_photo(
        Aaru, 
        caption = startText,
        reply_markup=t.InlineKeyboardMarkup(
            [
                [
                    t.InlineKeyboardButton(text="Support",url="https://t.me/Ahjin_sprt")
                ]
            ]
        )
    )