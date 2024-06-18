import io
import os
from re import sub
import sys
import traceback
from config import 
from pyrogram.errors import RPCError
import subprocess
from datetime import datetime
from pyrogram import filters, enums, Client


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@Client.on_message(filters.command(["eval", "ex", "ev", "xeval"]))
async def eval(client, message):
    try:
        user_id = message.from_user.id
    except:
        return
    if user_id not in DEVS:
        return
    if len(message.text.split()) < 2:
        return await message.reply_text("**ɪɴᴘᴜᴛ ɴᴏᴛ ғᴏᴜɴᴅ!**")

    cmd = message.text.split(maxsplit=1)[1]     
    status_message = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ...**")    
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "**sᴜᴄᴄᴇss**"
    end = datetime.now()
    ping = (end-start).microseconds / 1000
    final_output =  "ɪɴᴘᴜᴛ: "
    final_output += f"{cmd}\n"
    final_output += "ᴏᴜᴛᴘᴜᴛ:\n"
    final_output += f"{evaluation.strip()}\n"
    final_output += f"ᴛᴀᴋᴇɴ ᴛɪᴍᴇ: {ping}ms"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await status_message.edit_text(final_output)


@Client.on_message(filters.command(["sh","shell"]))
async def shell(client, message):
    if message.from_user.id not in DEVS:
        return
    cmd = message.text.split(" ")
    if len(cmd) == 1:
        await message.reply_text("ɴᴏ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀs ɢɪᴠᴇɴ ᴛᴏ ʀᴜɴ!")
        return
    cmd = message.text.split(None, 1)[1]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    stdout, stderr = process.communicate()
    reply = ""
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        reply += f"**sᴛᴅᴏᴜᴛ**\n`{stdout}`\n"
    if stderr:
        reply += f"**sᴛᴅᴇʀʀ**\n`{stderr}`\n"
    if len(reply) > 3000:
        with open("shell_output.txt", "w") as file:
            file.write(reply)
        with open("shell_output.txt", "rb") as doc:
            await messsage.reply_document(
                document=doc,
                caption="sʜᴇʟʟ ᴏᴜᴛᴘᴜᴛ"
            )
        if os.path.isfile("shell_ouput.txt"):
            os.remove("shell_output.txt")
    else:
        await message.reply_text(reply)