from pyrogram import Client, filters
import ast

@Client.on_message(filters.command("eval"))
def eval(client, message):
    try:
        code = message.text.split(" ", 1)[1]
        result = eval(ast.parse(code, mode="exec"))
        message.reply(f"**Output:** ```{result}```")
    except Exception as e:
        message.reply(f"**Error:** ```{e}```")