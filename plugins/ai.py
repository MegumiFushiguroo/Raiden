# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import getText,ChatCompletion,getMedia,geminiVision
from lexica.constants import languageModels
from gtts import gTTS
import os, time
from pyrogram import Client as app
from pyrogram.enums import ChatAction

@Client.on_message(filters.command([i for i in dir(languageModels) if not i.startswith("__")]))
async def chatbots(_: Client,m: t.Message):
    prompt = getText(m)
    media = getMedia(m)
    if media is not None:
        return await askAboutImage(_,m,[media],prompt)
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    model = m.command[0].lower()
    output = await ChatCompletion(prompt,model)
    if model == "bard":
        output, images = output
        if len(images) == 0:
            return await m.reply_text(output)
        media = []
        for i in images:
            media.append(t.InputMediaPhoto(i))
        media[0] = t.InputMediaPhoto(images[0],caption=output)
        await _.send_media_group(
            m.chat.id,
            media,
            reply_to_message_id=m.id
            )
        return
    await m.reply_text(output[0]['text'] if model=="gemini" else output)

async def askAboutImage(_:Client,m:t.Message,mediaFiles: list,prompt:str):
    images = []
    for media in mediaFiles:
        image = await _.download_media(media.file_id,file_name=f'./downloads/{m.from_user.id}_ask.jpg')
        images.append(image)
    output = await geminiVision(prompt if prompt else "whats this?","geminiVision",images)
    await m.reply_text(output)


@Client.on_message(filters.command(["assis"],  prefixes=["+", ".", "/", "-", "?", "$","#","&"]))
async def chat(Client : Client, message):

    try:
        start_time = time.time()
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "**Hello! How can I assist you today?**")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            text = x    
            tts = gTTS(text, lang='en')
            tts.save('output.mp3')
            await app.send_voice(chat_id=message.chat.id, voice='output.mp3')
            os.remove('output.mp3')            

    except Exception as e:
        await message.reply_text(f"**Error**: {e} ") 
