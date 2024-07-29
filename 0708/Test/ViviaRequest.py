import requests
import Tool as tool
import json

currentTaskId = ""
batchCallBack = None
downloadTargetPath = ""
taskFinishCallback = None

def configDownloadPath(path):
    global downloadTargetPath
    print(f"CONFIG DOWNLOAD PATH = {path}")
    downloadTargetPath = path

def doEventRequest():
    url = 'https://vivago.ai/api/dc/v1/events'

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    headers = {
        'X-Token' : token
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

    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    cookie = '_ga=GA1.1.793964204.1716263546; g_state={"i_l":0}; ticket=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJjcmVhdGVfdGltZSI6IjIwMjQtMDUtMjFUMDM6NTI6NDcuOTc5MzcxKzAwOjAwIiwibm9uY2UiOiI5MzU1In0._vxDkEYTplxTGFbWR73NZjk9tgKv0pK9i601c82dSQc; device_id=ab93cad8-2efb-477e-b958-f506586cd078; Hm_lvt_a4b926dc28419a9832df7388449e3efb=1721613058,1721624631,1721645740,1721692246; Hm_lpvt_a4b926dc28419a9832df7388449e3efb=1721692246; HMACCOUNT=08C7AD122FA2072F; _ga_60NXN3JTJS=GS1.1.1721692245.32.0.1721692245.60.0.1152086003'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        'X-Token' : token,
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
    cookie = '_ga=GA1.1.793964204.1716263546; g_state={"i_l":0}; ticket=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJjcmVhdGVfdGltZSI6IjIwMjQtMDUtMjFUMDM6NTI6NDcuOTc5MzcxKzAwOjAwIiwibm9uY2UiOiI5MzU1In0._vxDkEYTplxTGFbWR73NZjk9tgKv0pK9i601c82dSQc; device_id=ab93cad8-2efb-477e-b958-f506586cd078; Hm_lvt_a4b926dc28419a9832df7388449e3efb=1721613058,1721624631,1721645740,1721692246; Hm_lpvt_a4b926dc28419a9832df7388449e3efb=1721692246; HMACCOUNT=08C7AD122FA2072F; _ga_60NXN3JTJS=GS1.1.1721692245.32.0.1721692245.60.0.1152086003'
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
    cookie = '_ga=GA1.1.793964204.1716263546; g_state={"i_l":0}; ticket=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJjcmVhdGVfdGltZSI6IjIwMjQtMDUtMjFUMDM6NTI6NDcuOTc5MzcxKzAwOjAwIiwibm9uY2UiOiI5MzU1In0._vxDkEYTplxTGFbWR73NZjk9tgKv0pK9i601c82dSQc; device_id=ab93cad8-2efb-477e-b958-f506586cd078; Hm_lvt_a4b926dc28419a9832df7388449e3efb=1721613058,1721624631,1721645740,1721692246; Hm_lpvt_a4b926dc28419a9832df7388449e3efb=1721692246; HMACCOUNT=08C7AD122FA2072F; _ga_60NXN3JTJS=GS1.1.1721692245.32.0.1721692245.60.0.1152086003'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        'X-Token' : token,
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
    doEventRequest()
    doSyncRequest(imagePath)

#begin()