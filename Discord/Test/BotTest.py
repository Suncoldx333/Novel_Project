from discord.ext import commands
import discord

import os
from urllib.parse import quote_plus
import json
import re
import Test_Const as Const
import asyncio

import time
from datetime import datetime

import tkinter as tk
import multiprocessing
import threading

discord_token2 = "MTI1ODMxNDY4OTQ0OTAzMzcyOA.GOaidz.nmPbqQKgJzyFYdzubwvxKPMFFroZRN3iD1rH9M"

doPoll = False
counter = 0

parent_conn = None
child_conn = None

def run_discord_botByQueue(token,queue):
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user.name}')
        if queue:
            print(f"WILL SEND CHILD AT {datetime.now()}")
            sessionid = client.user.name
            queue.put(sessionid)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    async def main():
        async with client:
            await client.start(token)

    asyncio.run(main())

def run_discord_bot(token,conn):
    print(f"CHILD CONN = {id(conn)}")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        if conn:
            print(f"WILL SEND CHILD AT {datetime.now()}")
            conn.send(client.user)
            conn.close()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    async def main():
        async with client:
            await client.start(token)

    asyncio.run(main())

def poll_pipe(pipe):
    while True:
        if pipe:
            time.sleep(10)
            print(f"CHECK PARENT PIPE POLL AT TIME :{datetime.now()}")
            if pipe.poll():  # 检查管道中是否有数据
                data = pipe.recv()
                print(f'Received data from child process: {data}')
                break
            else:
                print(pipe.poll())
        time.sleep(1)  # 避免过度消耗CPU，可根据需要调整轮询间隔
    pipe.close()

def start_bot(token):
    global parent_conn,child_conn
    parent_conn,child_conn = multiprocessing.Pipe()
    print(f"PARENT = {id(parent_conn)},CHILD = {id(child_conn)}")

    p = multiprocessing.Process(target=run_discord_bot, args=(token,child_conn))
    p.start()
    #p.join()

    if parent_conn:
        # 创建并启动轮询线程
        print("CREATE THREADING")
        t = threading.Thread(target=poll_pipe, args=(parent_conn,))
        t.daemon = True  # 设置为守护线程，这样主线程退出时它也会自动退出
        t.start()
       # t.join()

    
    return p

def child_process(queue,token):

    run_discord_botByQueue(token,queue)


def thread_function(queue):
    while True:
        if not queue.empty():
            message = queue.get()
            print(f"Thread received: {message}")
            break  # 收到特定消息后退出
        else:
            print("Thread: No data yet.")
        time.sleep(0.5)  # 短暂等待

if __name__ == '__main__':
    # 你的Discord Bot Token
    token = discord_token2

    root = tk.Tk()
    root.title("Discord Bot Controller")
    windowWidth = 1000
    windowHeight = 800

    root.geometry(f"{windowWidth}x{windowHeight}+100+100")

    def on_button_click():
        # 当按钮被点击时，开始Bot

        queue = multiprocessing.Queue()

        # 创建子进程
        p = multiprocessing.Process(target=child_process, args=(queue,discord_token2))
        p.start()

        # 创建新线程
        t = threading.Thread(target=thread_function, args=(queue,))

        #global bot_process
        #bot_process = start_bot(token)
        button.config(text="Bot Started", state=tk.DISABLED)

    def thread_dopoll():
        while doPoll:
            print("POLLING~~~")
            time.sleep(1)

    def on_button_click2():
    # 当按钮被点击时，开始Bot
        print("123")

    button = tk.Button(root, text="Start Bot", command=on_button_click)
    button.pack()
    button2 = tk.Button(root, text="TEST Bot", command=on_button_click2)
    button2.pack()


    root.mainloop()

    # 当GUI窗口关闭时，确保等待Bot进程结束