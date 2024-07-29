import requests
import json
import time

import asyncio
import aiohttp

global_taskId = ""

async def fetchdata(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()

            await handle_data(data)

async def handle_data(data):
    print("处理数据", data)





def createHero(des):
    imagine(des)

def imagine(promt):

    totalpro = "Ink Wash Painting Style, " + promt + " --v 6.0 --ar 16:9"
    print("\n PTOMT = " + totalpro + "\n")
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
            "prompt": totalpro,
            "remix": True,
            "state": ""
        }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    print(result)
    dic = json.loads(result)
    taskid = dic['result']
    global global_taskId
    global_taskId = taskid
    #print("---now----" + str(time.time()))
    #time.sleep(5)
    #print("---now----" + str(time.time()))
    #progress = fetch(global_taskId)
    dic = {"taskId" : global_taskId,"progress" : "weee"}
    print(dic)
    return dic

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
    print(dic)

    progress = dic['progress']
    print("progress = " + progress)

    imageUrl = dic['imageUrl']
    print("imageUrl = " + imageUrl)

    resultDic = {'progress' : progress}
    if len(imageUrl) > 0 :
        resultDic['imageUrl'] = imageUrl

    print(resultDic)
    return resultDic

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
'''
ttid = "1715775133377489"
ccid = "MJ::JOB::upsample::1::1fd87706-a4f1-4204-a916-721374e31842"
action(ttid,ccid)
'''
#imagine()