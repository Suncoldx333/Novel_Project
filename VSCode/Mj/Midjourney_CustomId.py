import requests
import json
import time
import random

import Mid_Const as Const


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

    status = dic['status']
    if status == 'NOT_START':
        Const.customPrint("NOT_START")
        #再次提交
        callback("0%",taskId,"",status)
    else:

        progress = dic['progress']
        if progress == None or progress == "":
            progress = "0%"

        imageUrl = dic['imageUrl']
        if imageUrl == None or imageUrl == "":
            imageUrl = ""


        callback(progress,taskId,imageUrl,status)

#fetch("1715776613815119")
'''
ttid = "1715775133377489"
ccid = "MJ::JOB::upsample::1::1fd87706-a4f1-4204-a916-721374e31842"
action(ttid,ccid)
'''
#imagine()