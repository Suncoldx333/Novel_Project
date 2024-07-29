import requests
import json
import time
import random

import SD_Const as Const

def fetchModels(mainurl,callback):
    url = mainurl + "/sdapi/v1/sd-models"

    headers = {
        "Content-Type": "application/json",
        }

    response = requests.get(url,headers=headers)
    result = response.content.decode("utf-8")
    callback(result)

def SD_ImageWithPrompt(mainUrl,prompt,simpler_Hash,filename,callBack):
    url = mainUrl + "/sdapi/v1/txt2img"
    headers = {
        "Content-Type": "application/json",
        }
    data = {
            "prompt": prompt,
            "batch_size": 3,
            "sd_model_hash": simpler_Hash,
            "width": 1600,
            "height": 900,
            "enable_hr": False

        }
    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    Const.log("FINISH DRAW REQUST -----------")

    dict =json.loads(result)
    images = dict["images"]
    count = len(images)
    Const.log("Image count = " + str(count))

    callBack()
    
    dict =json.loads(result)
    images = dict["images"]
    timestamp = time.time()
    timestamp_int = int(timestamp)
    for image in images:
        Const.base2img(image,str(timestamp_int))


def checkprogress(mainUrl,callback):
    Const.log("CHECK PROGRESS")

    url = mainUrl + "/sdapi/v1/progress"
    headers = {
        "Content-Type": "application/json",
        }
    data = {
            "skip_current_image": False,
        }
    response = requests.get(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    #Const.log(result)
    dic = json.loads(result)

    callback(dic)




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
