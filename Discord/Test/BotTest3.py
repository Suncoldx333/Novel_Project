
import discord

discord_token2 = "MTI1ODMxNDY4OTQ0OTAzMzcyOA.GOaidz.nmPbqQKgJzyFYdzubwvxKPMFFroZRN3iD1rH9M"


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f"GET MESSAGE = {message.content}")

client.run(discord_token2)