from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
from discord.http import HTTPClient, Route
import aiohttp
from urllib.parse import quote_plus
import json
import re

discord_token = "MTI1NTY5NDAxNjYyMDUzMTc0Mg.GcJW3p.fY_BtsZP_6XvqeRoWRsplkghsYxooMQe3bFxYc"
# 假设用户名和密码中包含特殊字符
username = "1073138529@qq.com"
password = "Suncoldx33"

# 对用户名和密码进行URL编码
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# 构建带有认证信息的代理URL
proxy_address = f"http://{encoded_username}:{encoded_password}@127.0.0.1:33210"
proxy_address2 = f"http://{encoded_username}:{encoded_password}@127.0.0.1:33210"
print(proxy_address)

login_callback = None
on_message_callback = None
for_single_callback = None
progress_callback = None

class MyClient(discord.Client):
    async def on_ready(self):
        # 当 bot 准备就绪时，打印 session_id
        session_id = self.ws.session_id
        print(f'Session ID: {session_id}')
        global login_callback
        if login_callback:
            login_callback()

client = MyClient()

def Login(callback):
    print("LOGIN")
    global login_callback
    login_callback = callback
    client.run(discord_token)

'''
class ProxyHTTPClient(HTTPClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connector = aiohttp.TCPConnector(limit=0, verify_ssl=True)
        self._session = aiohttp.ClientSession(connector=self.connector)

    async def request(self, route: Route, *, files=None, **kwargs):
        method = route.method
        url = route.url
        headers = kwargs.pop('headers', {})
        if self.token is not None:
            headers['Authorization'] = 'Bot ' + self.token

        if isinstance(files, dict):
            if len(files) > 0:
                form = []
                for key, file in files.items():
                    form.append(
                        aiohttp.FormData(quote_fields=False)
                        .add_field('payload_json', json.dumps(kwargs['json'] or {}))
                        .add_field(key, file.fp, filename=file.filename, content_type='application/octet-stream')
                    )
                    kwargs['data'] = form
                del kwargs['json']

        response = await self._session.request(method, url, headers=headers, proxy=proxy_address, **kwargs)
        data = await response.text(encoding='utf-8')
        if response.status == 204:
            return None
        if not 200 <= response.status < 300:
            raise discord.HTTPException(response, data)
        return data

    async def close(self):
        await self._session.close()
'''



#load_dotenv()


'''
intent = discord.Intents.default()
intent.message_content = True
client = commands.Bot(command_prefix='',intents=intent)
directory = os.getcwd()
print(f"directory = {directory}")
#--------CLIENT EVETN----------------------


@client.event
async def on_ready():
    print("Bot connected")
    global login_callback
    if login_callback:
        print("123")
        login_callback()
    else:
        print("234")
'''

@client.event
async def on_message(message):

    for attachment in message.attachments:

        if message.components:
            print("has components")
            bigarray = []
            for component in message.components:
                array = []
                for index, child in enumerate(component.children):
                    customId = child.custom_id
                    array.append(customId)
                bigarray.append(array)

        if "Upscaled by" in message.content:
            print('UPSCALE')
        else:
            print("------------------")
            #print('NORMAL')
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            Imageurl = ""
            if message.attachments:
                for attachment in message.attachments:
                    Imageurl = attachment.url
                    if Imageurl == "":
                        print("EMPTY IMAGE URL")
                    else:
                        break

            staticSession_id = "653e36a26348f6ee666f6ebdfa8af9b5"
            staticApplication_id = "936929561302675456"
            
            if on_message_callback:
                #await client.close()
                #print('BOT CLOSE')
                on_message_callback(message.id, message.guild.id,
                                    message.channel.id, staticSession_id,
                                    staticApplication_id, bigarray)
            elif for_single_callback:
                for_single_callback(Imageurl)

            #on_message_callback = None
            #for_single_callback = None
            
@client.event
async def on_message_edit(before, after):
    global progress_callback
    print("------------------")
    print("ON MESSAGE EDIT")
    if before.content != after.content:
        #channel = after.channel
        content = after.content
        progress = extract_first_substring(content)
        print(f"Progress : {progress}")
        if progress:
            pro = progress[:-1]
            pro_int = int(pro)

        if progress_callback:
            progress_callback(progress)



#------------CONFIG CALLBACK-------------------

def config_progress_callBack(callback):
    global progress_callback
    progress_callback = callback

def config_messsage_callBack(callback):
    global on_message_callback
    on_message_callback = callback

def config_message_edit_callBack(callback):
    global for_single_callback
    for_single_callback = callback


def extract_first_substring(s):
    # 使用正则表达式寻找第一个匹配项
    pattern = r'\((.+?)\)'
    match = re.search(pattern, s)

    # 如果找到匹配项，则返回第一个子串，否则返回None
    return match.group(1) if match else None
#client.run(discord_token)


def BotRunCallBack(mid,gid,cid,staticSession_id,staticApplication_id):
    print(f"mid = {mid},gid = {gid},cid = {cid},session = {staticSession_id},application = {staticApplication_id}")