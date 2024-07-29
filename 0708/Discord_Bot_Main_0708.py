import tkinter as tk
import discord
import asyncio
import threading
from datetime import datetime
import json

import Bot_Data_0708
from Bot_Data_0708 import DataType
from Bot_Data_0708 import DataFromBot as Data_B
from Bot_Data_0708 import CustomIdObject
from Bot_Data_0708 import ImageUrlObject

import re

discord_token2 = "none"

sessionidCallback = None
afterCallback = None
drawCallback = None
fetchFourCustomidCallback = None
progressCallback = None
fetchCustomIdCallback = None
fetchCustomImageUrlCallback = None


IsDrawingFour = False
isDrawingSingle = True

intent = discord.Intents.default()
intent.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        # 当 bot 准备就绪时，打印 session_id
        session_id = self.ws.session_id
        #print(f'Session ID: {session_id}')
        
        data = Data_B(DataType.SESSION_ID,session_id)
        #print(f"CREATE DATA = {data}")
        await queue.put(data)  # 将 bot 名称放入队列
        #await client.close()  # 获取到名称后关闭客户端

    async def custom_reconnect(self):
        # 在这里放置你的重连逻辑
        # 注意：不要在这里进行长时间的阻塞操作
        # 你可以使用asyncio.sleep()来避免立即重连
        await asyncio.sleep(5)  # 延迟5秒后重连
        try:
            await self.ws.resume()
        except Exception as e:
            print(f"Failed to reconnect: {e}")
    
    async def on_disconnect(self):
        print("Disconnected from Discord. Attempting to reconnect...")
        asyncio.create_task(self.custom_reconnect())

client = MyClient(intents=intent)

@client.event
async def on_message(message):
    global sessionId
    print("ON_MESSAGE")
    if message.attachments:
            for attachment in message.attachments:
                url = attachment.url
                print(f"URL = {url}")
    
    if IsDrawingFour:
        if message.components:
                print("has components")
                bigarray = []
                customId = {
                    "messageid" : message.id,
                    "guildid" : message.guild.id,
                    "channelid" : message.channel.id,
                    "bigarray" : [] 
                }
                str = ""
                for component in message.components:
                    array = []
                    for index, child in enumerate(component.children):
                        customId = child.custom_id
                        array.append(customId)
                    bigarray.append(array)
                    #customId['bigarray'] = bigarray
                    str = json.dumps(bigarray)
                    #print(f"CUSTOMID = {str}")
                data = CustomIdObject(DataType.CUSTOMID,message.id,message.guild.id,message.channel.id,str)
                #print(f"data = {data}")
                await queue.put(data)
    elif isDrawingSingle:
        if message.attachments:
            url = ""
            for attachment in message.attachments:
                url = attachment.url
                break
            data = ImageUrlObject(DataType.IMAGEURL,url)
            #print(f"data = {data}")
            await queue.put(data)

@client.event
async def on_message_edit(before, after):

    if before.content != after.content:
        #channel = after.channel
        content = after.content
        #print(f"AFTER = {content}")
        progress = extract_first_substring(content)
        #print(f"Progress : {progress}")
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

def configDrawingState(four,signle):
    global IsDrawingFour
    global isDrawingSingle

    IsDrawingFour = four
    isDrawingSingle = signle

def configFetchCustomIdCallback(callback):
    global fetchCustomIdCallback

    fetchCustomIdCallback = callback

def configFetchCustomImageUrlCallback(callback):
    global fetchCustomImageUrlCallback

    fetchCustomImageUrlCallback = callback

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
        data = queue.get_nowait()
        #print(f"GET DATA = {data}")
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
        elif dataType == DataType.CUSTOMID:
            global fetchCustomIdCallback
            if fetchCustomIdCallback:
                print("CALLBACK")
                fetchCustomIdCallback(data)
        elif dataType == DataType.IMAGEURL:
            if fetchCustomImageUrlCallback:
                fetchCustomImageUrlCallback(data)

    except asyncio.QueueEmpty:
        #print("NO DATA")
        if a_callback:
            a_callback()
        else:
            print("NO CALLBACK")
