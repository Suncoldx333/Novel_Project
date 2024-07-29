import tkinter as tk
import multiprocessing
import discord
import asyncio

discord_token2 = "MTI1ODMxNDY4OTQ0OTAzMzcyOA.GOaidz.nmPbqQKgJzyFYdzubwvxKPMFFroZRN3iD1rH9M"
parent_conn = None

def run_discord_bot(token,conn):
    class MyClient(discord.Client):
        async def on_ready(self):
            # 当 bot 准备就绪时，打印 session_id
            session_id = self.ws.session_id
            conn.send([session_id])
            conn.close()
            print(f'Session ID: {session_id}')

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

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

def start_bot(token):

    doQuest()
    global parent_conn,child_conn
    parent_conn,child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=run_discord_bot, args=(token,child_conn))
    p.start()

    return p

def callback(sessionid):
    print(f"CALLBACK SESSION ID = {sessionid}")

def doQuest():
    print("CHECK PIPE")
    if parent_conn:
        if parent_conn.poll():
            result = parent_conn.recv()
            print(f"GOT SESSION ID = {result}")
        else:
            root.after(300, doQuest)
    else:
        print("NO PARENT PIPE")
        root.after(300, doQuest)

if __name__ == '__main__':
    # 你的Discord Bot Token
    token = discord_token2

    root = tk.Tk()
    root.title("Discord Bot Controller")
    root.geometry(f"500x400+100+100")



    def on_button_click():
        # 当按钮被点击时，开始Bot
        global bot_process
        bot_process = start_bot(token)
        button.config(text="Bot Started", state=tk.DISABLED)

    def testlog():
        print("123")

    button = tk.Button(root, text="Start Bot", command=on_button_click)
    button.pack()

    button2 = tk.Button(root, text="Start Bot1223", command=testlog)
    button2.pack()

    def check_pipe():
        print("CHECK PIPE")
        if parent_conn and parent_conn.poll():
            result = parent_conn.recv()
            if result == 'Finished':
                print("Worker has finished.")
                # 这里可以调用一个回调函数或执行其他操作
            print(f"GOT SESSION ID = {result}")
        else:
            print("NO PARENT PIPE")
        #root.after(1500, check_pipe)  # 每1500毫秒检查一次管道

    #root.after(3000, check_pipe)

    root.mainloop()

    # 当GUI窗口关闭时，确保等待Bot进程结束
    if 'bot_process' in globals() and bot_process.is_alive():
        bot_process.join()