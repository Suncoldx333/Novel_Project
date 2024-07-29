import tkinter as tk
import discord
import asyncio
import threading
from datetime import datetime

import Bot_Data
from Bot_Data import DataType
from Bot_Data import DataFromBot as Data_B
import re

discord_token2 = "MTI1ODMxNDY4OTQ0OTAzMzcyOA.GOaidz.nmPbqQKgJzyFYdzubwvxKPMFFroZRN3iD1rH9M"

sessionidCallback = None
afterCallback = None
drawCallback = None
progressCallback = None

intent = discord.Intents.default()
intent.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        # 当 bot 准备就绪时，打印 session_id
        session_id = self.ws.session_id
        print(f'Session ID: {session_id}')
        
        data = Data_B(DataType.SESSION_ID,session_id)
        print(f"CREATE DATA = {data}")
        await queue.put(data)  # 将 bot 名称放入队列
        #await client.close()  # 获取到名称后关闭客户端

client = MyClient(intents=intent)

@client.event
async def on_message(message):
    global sessionId
    if message.content == "":
        if message.attachments:
            print("This message has attachments:")
            for attachment in message.attachments:
                print(attachment.url)
        elif message.embeds:
            print("This message has embeds:")
            for embed in message.embeds:
                print(embed.title)
        else:
            print("The message does not contain any text or media.")
    else:
        print(f"Received a message: {message.content}")

@client.event
async def on_message_edit(before, after):

    if before.content != after.content:
        #channel = after.channel
        content = after.content
        print(f"AFTER = {content}")
        progress = extract_first_substring(content)
        print(f"Progress : {progress}")
        if progress:
            pro = progress[:-1]
            data = Data_B(DataType.PROGRESS,pro)
            await queue.put(data)

def extract_first_substring(s):
    # 使用正则表达式寻找第一个匹配项
    pattern = r'\((.+?)\)'
    match = re.search(pattern, s)
    return match.group(1) if match else None


# 创建一个队列以便跨线程通信
queue = asyncio.Queue()

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

def configProgressCallback(callback):
    global progressCallback
    progressCallback = callback


# 按钮点击事件处理函数
def drawImage(d_callback):

    global drawCallback
    drawCallback = d_callback

    loop = asyncio.new_event_loop()
    token = discord_token2  # 替换为你的 bot token
    thread = threading.Thread(target=start_discord_bot, args=(loop, token))
    thread.start()

# 按钮点击事件处理函数
def on_button_click(a_callback,s_callback):

    global sessionidCallback
    sessionidCallback = s_callback

    global afterCallback
    afterCallback = a_callback

    loop = asyncio.new_event_loop()
    token = discord_token2  # 替换为你的 bot token
    thread = threading.Thread(target=start_discord_bot, args=(loop, token))
    thread.start()
    
    check_queue(a_callback)
    
# 检查队列并更新标签
def check_queue(a_callback):
    try:
        #print("CHECK QUEUE")
        data = queue.get_nowait()
        print(f"GET DATA = {data}")
        dataType = data.type
        if dataType == DataType.SESSION_ID:
            sessionid = data.data
            print(f"TYPE = {dataType}")

            global sessionidCallback
            if sessionidCallback:
                sessionidCallback(sessionid)
        elif dataType == DataType.PROGRESS:
            progress = data.data
            print(f"PROGRESS = {progress}")

            global progressCallback
            if progressCallback:
                progressCallback(progress)
        
    except asyncio.QueueEmpty:
        #print("NO DATA")
        a_callback()

'''
# Tkinter 界面设置
root = tk.Tk()
root.title("Discord Bot Name Fetcher")

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+100+100")

label = tk.Label(root, text="Bot Name: Not fetched yet")
label.pack(pady=10)

button = tk.Button(root, text="Fetch Bot Name", command=on_button_click)
button.pack(pady=10)

root.mainloop()

'''