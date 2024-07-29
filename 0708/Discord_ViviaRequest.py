import requests
import Discord_Tool as tool
import json
import os

currentTaskId = ""
batchCallBack = None
downloadTargetPath = ""
taskFinishCallback = None

cookie_g = ""

def configDownloadPath(path):
    global downloadTargetPath
    print(f"CONFIG DOWNLOAD PATH = {path}")
    downloadTargetPath = path

def doEventRequest(callback):
    url = 'https://vivago.ai/api/dc/v1/events'

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    global cookie_g
    cookie = cookie_g
    headers = {
        #'X-Token' : token
        'Cookie' : cookie,
    }

    timestamp = tool.getTimeStampe()

    data = {
        "channel_id": "qx_pc",
        "user_id": "7b56234d-2d41-43f1-b880-a5cd547dd3f4",
        "device_id": "ab93cad8-2efb-477e-b958-f506586cd078",
        "event_time": timestamp,
        "event_id": "img2video",
        "page_name": "aigc_studio",
        "device": "pc"
    }

    response = requests.post(url,json=data,headers=headers)
    result = response.content.decode("utf-8")

    print(f"Code = {response.status_code},result = {result}")
    callback(response.status_code)

def doPureEventRequest():
    url = 'https://vivago.ai/api/dc/v1/events'

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    global cookie_g
    cookie = cookie_g
    headers = {
        #'X-Token' : token
        'Cookie' : cookie,
    }

    timestamp = tool.getTimeStampe()

    data = {
        "channel_id": "qx_pc",
        "user_id": "7b56234d-2d41-43f1-b880-a5cd547dd3f4",
        "device_id": "ab93cad8-2efb-477e-b958-f506586cd078",
        "event_time": timestamp,
        "event_id": "img2video",
        "page_name": "aigc_studio",
        "device": "pc"
    }

    response = requests.post(url,json=data,headers=headers)
    result = response.content.decode("utf-8")

    print(f"Code = {response.status_code},result = {result}")


def doSyncRequest(imagepath):
    url = 'https://vivago.ai/api/gw/v2/video/video_diffusion/async'
    global cookie_g
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    cookie = cookie_g
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        #'X-Token' : token,
        'Cookie' : cookie,
        'User-Agent' : user_agent
    }

    path = imagepath
    imagebase64 = tool.getImageBase64Code(path)

    request_id = tool.getUuid()

    data = {
        "image": imagebase64,
        "module": "video_diffusion",
        "params": {
            "batch_size": 1,
            "guidance_scale": 7,
            "sample_steps": 80,
            "width": 768,
            "height": 432,
            "frame_num": 16,
            "seed": -1,
            "motion_strength": 7,
            "max_width": 1024,
            "wh_ratio": "16:9",
            "cm_x": 0,
            "cm_y": 0,
            "cm_d": 0
        },
        "prompt": "wind,bird,rain",
        "negative_prompt": "",
        "role": "general",
        "style": "default",
        "wh_ratio": "16:9",
        "request_id": request_id
    }

    response = requests.post(url,json=data,headers=headers)
    result = response.content.decode("utf-8")

    print(f"Code = {response.status_code},result = {result}")
    resultDic = json.loads(result)
    taskid = resultDic['result']['task_id']
    global currentTaskId
    currentTaskId = taskid

    print(f"taskid = {taskid}")
    doResultRequest(taskid)

def doResultRequest(taskid):
    url = 'https://vivago.ai/api/gw/v2/video/video_diffusion/async/results?task_id=' + taskid

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    global cookie_g
    cookie = cookie_g
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        'X-Token' : token,
        'Cookie' : cookie,
        'User-Agent' : user_agent
    }

    response = requests.get(url,headers=headers)
    result = response.content.decode("utf-8")

    print(f"Code = {response.status_code},result = {result}")

    if response.status_code == 200:
        doBatchRequest(taskid)

def doBatchRequest(taskid):
    global currentTaskId
    global batchCallBack


    if taskid == "" and currentTaskId != "":
        taskid = currentTaskId

    url = 'https://vivago.ai/api/gw/v2/video/video_diffusion/async/results/batch'

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    global cookie_g
    cookie = cookie_g
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        #'X-Token' : token,
        'Cookie' : cookie,
        'User-Agent' : user_agent
    }

    data = {
        'task_id_list' : [
            taskid
        ]
    }

    response = requests.post(url,json=data,headers=headers)
    result = response.content.decode("utf-8")

    print(f"Code = {response.status_code},result = {result}")

    resultDic = json.loads(result)
    completion = resultDic['result'][0]['sub_task_results'][0]['task_completion']
    print(f"Completion = {str(completion)}")

    if completion == 1:
        batchCallBack = None
        vedioname = resultDic['result'][0]['sub_task_results'][0]['video']
        doDownload(vedioname)
    else:
        print(f"COMPLETION = {completion}")
        if batchCallBack:
            batchCallBack()



def doDownload(filename):
    global downloadTargetPath
    url = 'https://media.vivago.ai/' + filename
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        'User-Agent' : user_agent
    }

    response = requests.get(url,headers=headers,stream=True)
    if response.status_code == 200:
        if not os.path.exists(downloadTargetPath):
            os.makedirs(downloadTargetPath)

        targetpath = downloadTargetPath + '/' + filename
        # 以二进制模式打开文件（写模式）
        with open(targetpath, 'wb') as file:
            # 写入文件（可以分块写入以节省内存）
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
            
            global taskFinishCallback
            if taskFinishCallback:
                taskFinishCallback(True)
    else:
        print(f"FAIL WITH CODE : {response.status_code}")

def begin():
    #doEventRequest()
    #doSyncRequest()
    name = '4a54ac13-0cf6-46c1-9f41-552987656e32_wm.mp4'
    doDownload(name)

def beginWithImage(imagePath,callback,callback_2):
    global taskFinishCallback
    if taskFinishCallback == None:
        taskFinishCallback = callback_2

    global batchCallBack
    if batchCallBack == None:
        batchCallBack = callback
    #doPureEventRequest()
    doSyncRequest(imagePath)

#path = 'E:/hero/0724/zigong/Images/Downloads/6.jpg' 
#doSyncRequest(path)