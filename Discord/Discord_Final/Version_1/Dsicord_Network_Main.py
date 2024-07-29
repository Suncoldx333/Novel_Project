import requests
import json
import time

import base64
import cv2
import numpy as np
import random

url = "https://discord.com/api/v9/interactions"


params = {
    "application_id" : "936929561302675456",
    "guild_id" : "1255422192695509072",
    "channel_id": "1255422193249030236",
    "session_id" : "402ed12483da296b9020268bafe3b8ac",
    "data" : {
        "version" : "1237876415471554623",
        "id" : "938956540159881230",
        "name" : "imagine",
        "type" : 1,
        "options" : [{
                    "type" : 3,
                    "name" : "prompt",
                    "value" : "The nemesis arrives, and Yu Rang swiftly acts, delivering a lethal strike that fulfills his revenge. --v 6.0 --ar 16:9",
                    "attachments" : []
                       }]

    }
}
def configParam(param):
    print("CONFIG PARAN IN NETWORK")
    global params
    params = param

def changeSessionId(sessionId):
    global params
    params['session_id'] = sessionId

def drawWithPrompt(prompt,characterRef,callback):
    global params
    newprompt = "Ink Wash Painting Style,Cold light," + prompt + " --v 6.0 --ar 16:9 --cref " + characterRef
    params['data']['options'][0]['value'] = newprompt
    headers = {
        "Authorization" : "NzA5MzM0MjI1NjM1MjQ2MDky.GBRHSW.ehL9jxAqUYPIrfZpdYn_yRa5UMquDLaWVsdfcE"
    }
    print(params)
    return
    response = requests.post(url,json=params,headers=headers)
    result = response.content.decode("utf-8")
    print(f"result = {result},code = {response.status_code}")
    callback(response.status_code)


    


def compare_dicts(dict1, dict2):
    differences = {}
    
    # 查找仅在第一个字典中存在的键
    for key in dict1.keys():
        if key not in dict2 or dict1[key] != dict2[key]:
            differences[f"Only in dict1 or different: {key}"] = dict1[key]

    # 查找仅在第二个字典中存在的键
    for key in dict2.keys():
        if key not in dict1:
            differences[f"Only in dict2: {key}"] = dict2[key]
    
    return differences


def draw():
    print("BEGIN")
    headers = {
        "Authorization" : "NzA5MzM0MjI1NjM1MjQ2MDky.GBRHSW.ehL9jxAqUYPIrfZpdYn_yRa5UMquDLaWVsdfcE"

    }
    data2 = {
         "type": 3,
        #"nonce": "1257228453736873984",
        "guild_id": "1255422192695509072",
        "channel_id": "1255422193249030236",
        "message_flags": 0,
        "message_id": "1257315639379497035",
        "application_id": "936929561302675456",
        "session_id": "e443ab87f5f15acf2b7c84ad983892a1",
        "data": {
            "component_type": 2,
            "custom_id": "MJ::JOB::upsample::1::8fe2254b-d853-4fe4-aadb-92a30a8746cf"
            }
        }


    #response = requests.post(url, headers=headers, data=json.dumps(data2).encode('utf-8') )
    response = requests.post(url,json=data2,headers=headers)
    result = response.content.decode("utf-8")
    print(f"result = {result},code = {response.status_code}")

#draw()

def drawCustom(bigType,type,customId,guild_id,channel_id,message_id):
    print("CUSTOM")
    headers = {
        "Authorization" : "NzA5MzM0MjI1NjM1MjQ2MDky.GBRHSW.ehL9jxAqUYPIrfZpdYn_yRa5UMquDLaWVsdfcE"

    }
    data2 = {
        "type": 3,
        #"nonce": "1257214790363774976",
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_flags": 0,
        "message_id": message_id,
        "application_id": "936929561302675456",
        "session_id": "653e36a26348f6ee666f6ebdfa8af9b5",
        "data": {
            "component_type": type,
            "custom_id": customId
        }
    }
    response = requests.post(url,json=data2,headers=headers)
    result = response.content.decode("utf-8")
    print(f"result = {result},code = {response.status_code}")


def getMessages():
    url = "https://discord.com/api/v9/channels/1255422193249030236/messages?limit=1"
    headers = {
        "Authorization" : "NzA5MzM0MjI1NjM1MjQ2MDky.GBRHSW.ehL9jxAqUYPIrfZpdYn_yRa5UMquDLaWVsdfcE"
    }
    response = requests.get(url,headers=headers)
    result = response.content.decode("utf-8")
    array = json.loads(result)
    print(len(array))
    return
    first = array[0]
    components = first['components']   
    vs = components[0]
    innerComponents = vs['components']
    message_reference = first['message_reference']

    message_id = first['id']
    guild_id = message_reference['guild_id']
    channel_id = message_reference['channel_id']
    bigType = vs['type']
    if len(innerComponents) == 5:
        
        index = random.randint(0,3)
        choosen = innerComponents[index]
        for choosen in innerComponents:
            print(f"type = {choosen['type']},customid = {choosen['custom_id']}")
        type = choosen['type']
        customId = choosen['custom_id']

        print(f"choosen type = {type},customId = {customId}")
        drawCustom(bigType,type,customId,guild_id,channel_id,message_id)

#getMessages()
