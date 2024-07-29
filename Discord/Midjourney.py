import requests
import json

import random
import MidBot as Bot

url = "https://discord.com/api/v9/interactions"

messageid = ""
guildid = ""
channelid = ""
sessionid = ""
appid = ""

def InitBot():
    Bot.BotRun(BotRunCallBack)

def BotRunCallBack(mid,gid,cid,staticSession_id,staticApplication_id):
    global messageid,guildid,channelid,sessionid,appid

    print(f"mid = {mid},gid = {gid},cid = {cid},session = {staticSession_id},application = {staticApplication_id}")

    messageid = mid
    guildid = gid
    channelid = cid
    sessionid = staticSession_id
    appid = staticApplication_id

    getMessages()

def BotSingleCallBack(url):
    print(f"get image url = {url}")

def getMessages():
    global messageid,guildid,channelid,sessionid,appid

    url = "https://discord.com/api/v9/channels/1255422193249030236/messages?limit=1"
    headers = {
        "Authorization" : "NzA5MzM0MjI1NjM1MjQ2MDky.GBRHSW.ehL9jxAqUYPIrfZpdYn_yRa5UMquDLaWVsdfcE"
    }
    response = requests.get(url,headers=headers)
    result = response.content.decode("utf-8")
    array = json.loads(result)
    first = array[0]
    components = first['components']   
    vs = components[0]
    innerComponents = vs['components']
    #message_reference = first['message_reference']
    print(array)
    return
    if len(innerComponents) == 5:
        
        index = random.randint(0,3)
        choosen = innerComponents[index]
        for choosen in innerComponents:
            print(f"type = {choosen['type']},customid = {choosen['custom_id']}")
        type = choosen['type']
        customId = choosen['custom_id']

        print(f"choosen type = {type},customId = {customId}")
        drawCustom(3,type,customId,guildid,channelid,messageid,sessionid,appid)


def drawCustom(bigType,type,customId,guild_id,channel_id,message_id,sessionid,applicationid):
    print("CUSTOM")

    Bot.configCallback(BotSingleCallBack,True)

    headers = {
        "Authorization" : "NzA5MzM0MjI1NjM1MjQ2MDky.GBRHSW.ehL9jxAqUYPIrfZpdYn_yRa5UMquDLaWVsdfcE"

    }
    data2 = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": applicationid,
        "session_id": sessionid,
        "data": {
            "component_type": type,
            "custom_id": customId
        }
    }
    response = requests.post(url,json=data2,headers=headers)
    result = response.content.decode("utf-8")
    print(f"result = {result},code = {response.status_code}")

#InitBot()
getMessages()