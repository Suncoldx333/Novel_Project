import requests
import json
import time
import random

import Mid_Const as Const


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

def imagineWithPrompt(prompt,character,callback):

    combinedsPrompt = "Ink Wash Painting Style,Cold light," + prompt + " --v 6.0 --cref " + character + " --ar 16:9"
    print("final = " + combinedsPrompt + "\n")


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
            "prompt": combinedsPrompt,
            "remix": True,
            "state": ""
        }
    '''
    data = {
            "base64Array": [],
            "notifyHook": "",
            "prompt": combinedsPrompt,
            "state": "",
            "botType": "MID_JOURNEY"
        }
    '''
    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    print(result)
    dic = json.loads(result)
    taskid = dic['result']
    if taskid == None:
        taskid = ""
    code = dic['code']
    print("---now----" + str(time.time()))
    time.sleep(2)
    print("---now----" + str(time.time()))
    callback(code,taskid)



def fetch(taskId,callback):
    print("taskid = " + taskId + "\n")

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
    print("\n" + result + "\n")

    if False :
        Const.customPrint("IT IS SINGLE")
        iamgeUrl = dic['imageUrl']
        if imageUrl == None or imageUrl == "":
            imageUrl = ""
    else:
        buttons = dic['buttons']
        
        if buttons is None:
            Const.log("buttons is null")
            buttons = []

        progress = dic['progress']
        if progress == None or progress == "":
            progress = "0%"


        customId = ""
        if len(buttons) > 0:
            #count = len(buttons) - 1
            randomIndex = 0
            choisen = buttons[randomIndex]
            customId = choisen['customId']

        imageUrl = dic['imageUrl']
        if imageUrl == None or imageUrl == "":
            imageUrl = ""


    callback(progress,taskId,customId,imageUrl)


def fetchByCUSTOMId(customId,callback):
    #customId等于taskId

    print("taskid = " + customId + "\n")
    url = "https://api.openai-hk.com/fast/mj/task/" + customId + "/fetch"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
        }
    data = {
            "id": customId,
        }

    response = requests.get(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    dic = json.loads(result)

    print("\nfetchByCUSTOMId:\n" + result + "\n")

    imageurl = dic['imageUrl']
    if imageurl == None or imageurl == "":
        imageurl = ""

    progress = dic['progress']
    if progress == None or progress == "":
        progress = "0%"


    customId = ""

    callback(progress,customId,"",imageurl)

def action(taskId,customId,callback):

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

    Const.customPrint(result)

    dic = json.loads(result)

    code = dic['code']
    if code == 1:
        customTaskId = dic['result']
    else:
        customTaskId = taskId

    print("simple result = ------\n" + customTaskId)
    callback(code,customTaskId,customId)

#fetch("1715776613815119")


def actionTest(taskId,customId):

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

    Const.customPrint(result)

    dic = json.loads(result)

    customTaskId = dic['result']
    if customTaskId == None or customTaskId == "":
        customTaskId = ""

    print("simple result = ------\n" + customTaskId)

def fetchTest(taskId):
    print("taskid = " + taskId + "\n")

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
    print("\n" + result + "\n")

#fetchTest("1716800934637888")
#ccid = "MJ::JOB::upsample::3::2affabaf-1638-411a-b1fb-b3c98d403298"
#actionTest("1716797244254107",ccid)
'''
ttid = "1716519121148083"
ccid = "MJ::JOB::variation::1::a6051675-fa13-4e2f-8ab0-263fce71bbb1"
actionTest(ttid,ccid)
'''
#imagine()