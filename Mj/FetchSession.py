import discord

discord_token = "MTI1NTY5NDAxNjYyMDUzMTc0Mg.GcJW3p.fY_BtsZP_6XvqeRoWRsplkghsYxooMQe3bFxYc"
readercallback = None

class MyClient(discord.Client):
    async def on_ready(self):
        # 当 bot 准备就绪时，打印 session_id
        session_id = self.ws.session_id
        print(f'Session ID: {session_id}')
        global readercallback
        if readercallback:
            readercallback()
        
intents = discord.Intents.default()
client = MyClient(intents=intents)

# 然后运行你的 bot 或者客户端

@client.event
async def on_message(message):
    print("123")

def login(callback):

    global readercallback
    readercallback = callback

    client.run(discord_token)

    