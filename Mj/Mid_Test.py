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
        "options" : [{"type" : 3,
                      "name" : "prompt",
                      "value" : "The nemesis arrives, and Yu Rang swiftly acts, delivering a lethal strike that fulfills his revenge. --v 6.0 --ar 16:9",
                      "attachments" : []
                       }]

    }
}

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

getMessages()

'''
def image2base64():
    file_path = "E:/hero/outside/local_image.jpg"
    img = cv2.imread(file_path)
    img_bytes = cv2.imencode('.jpg',img)[1].tobytes()
    encode_img = base64.b64encode(img_bytes)

    decode_img_bytes = base64.b64decode(encode_img)
    decoded_img = cv2.imdecode(np.frombuffer(decode_img_bytes, np.uint8), cv2.IMREAD_COLOR)

    h,w,c = decoded_img.shape
    s_h = 1.5 * h
    s_w = 1.5 * w
    

    print (f"h,w = {s_h}x{s_w}")

    cv2.resize(decoded_img,(250,870))
    cv2.imshow('Decode Img',decoded_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows

    save_path = "E:/hero/outside/local_image34.jpg"


def imagine():

    url = "https://api.openai-hk.com/fast/mj/submit/imagine"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
        }
    data = {
            "base64Array": [],
            "instanceId": "",
            "modes": [],
            "notifyHook": "",
            "prompt": "Ink Wash Painting Style,Toweringly tall and upright, with a rugged visage etched in firm determination, his features are chiseled and resolute. His eyes are deep-set and piercing, betraying both wisdom and an unwavering resolve. Adorned with scars that tell tales of past battles, his hair and beard are streaked with white, imbuing him with a sense of seasoned experience. Clutching a longsword and clad in battle-hardened gear, he stands ever-ready to engage in combat. --v 6.0 --ar 16:9",
            "remix": True,
            "state": ""
        }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    print(result)
    dic = json.loads(result)
    taskid = dic['result']
    print("---now----" + str(time.time()))
    time.sleep(2)
    print("---now----" + str(time.time()))
    fetch(taskid)


def fetch(taskId):

    print("taskid = " + taskId)
    url = "https://api.openai-hk.com/fast/mj/task/" + taskId + "/fetch"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
        }
    data = {
            "id": taskId,
        }

    response = requests.get(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    dic = json.loads(result)

    print(result)

def action(taskId,customId):

    print("taskid = " + taskId)
    print("customid = " + customId)

    url = "https://api.openai-hk.com/fast/mj/submit/action"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
        }
    data = {
            "customId": customId,
            "notifyHook": "",
            "state": "",
            "taskId": taskId
        }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    dic = json.loads(result)

    print("simple result = ------\n" + result)

#fetch("1715776613815119")

ttid = "1715775133377489"
ccid = "MJ::JOB::upsample::1::1fd87706-a4f1-4204-a916-721374e31842"
action(ttid,ccid)
'''
