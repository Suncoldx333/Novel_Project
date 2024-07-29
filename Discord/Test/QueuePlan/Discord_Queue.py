import tkinter as tk
import discord
import asyncio
import threading

# Discord bot client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# 创建一个队列以便跨线程通信
queue = asyncio.Queue()

checkCallback = None

# on_ready 事件来获取 bot 名称
@client.event
async def on_ready():
    bot_name = client.user.name
    await queue.put(bot_name)  # 将 bot 名称放入队列
    await client.close()  # 获取到名称后关闭客户端

# 在新线程中启动 Discord bot
def start_discord_bot(loop, token):
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(client.start(token))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

def BotLogin(callback):
    global checkCallback
    checkCallback = callback

    loop = asyncio.new_event_loop()
    token = 'YOUR_BOT_TOKEN'  # 替换为你的 bot token
    thread = threading.Thread(target=start_discord_bot, args=(loop, token))
    thread.start()
    check_queue()


# 按钮点击事件处理函数
def on_button_click():
    loop = asyncio.new_event_loop()
    token = 'YOUR_BOT_TOKEN'  # 替换为你的 bot token
    thread = threading.Thread(target=start_discord_bot, args=(loop, token))
    thread.start()
    check_queue()

# 检查队列并更新标签
def check_queue():
    try:
        bot_name = queue.get_nowait()
        #label.config(text=f"Bot Name: {bot_name}")
    except asyncio.QueueEmpty:
        global checkCallback
        if checkCallback:
            checkCallback()
        #root.after(100, check_queue)