import requests
import Discord_Tool as tool
import json
import os
import glob
from Bot_Data_0708 import ViviaObject
import time
import threading

from tkinter import Tk,ttk, Frame, Scrollbar, Text,filedialog,Canvas,Label,StringVar,OptionMenu,messagebox
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
import tkinter as tk
'''
root = Tk()

windowWidth = 1000
windowHeight = 800

root.geometry(f"{windowWidth}x{windowHeight}+600+50")

button_bot = Button(root,text="START",command=lambda: start())
button_bot.pack()
'''

currentTaskId = ""
batchCallBack = None
downloadTargetPath = 'E:/hero/0724/zigong/Images/Downloads/Part'
taskFinishCallback = None

bool_ShouldStopAfer = False
rootafter_id = ""


cookie_g = '_ga=GA1.1.793964204.1716263546; g_state={"i_l":0}; Hm_lvt_a4b926dc28419a9832df7388449e3efb=1721624631,1721645740,1721692246,1721721751; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJjcmVhdGVfdGltZSI6IjIwMjQtMDUtMjFUMDM6NTI6NDcuOTc5MzcxKzAwOjAwIiwibm9uY2UiOiI5MzU1In0._vxDkEYTplxTGFbWR73NZjk9tgKv0pK9i601c82dSQc; ticket=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMjQwODkyMX0.pBvnxF9M0-ZrRe8ePw-Go9FlzqCa7NLLpuA9uc0xs0I; device_id=ddac2ab8-8e35-4939-99ed-f2a0281e1459; username=google_EjSxoGO; _ga_60NXN3JTJS=GS1.1.1721991813.35.1.1721992700.54.0.713715130'

groups = []
index = 0
downloadIndex = 0
MAXGROUPCOUNT = 2
batch = []
path = 'E:/hero/0724/zigong/Images/Downloads/Part' 

def start():
    doGroup(path)

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

def doSyncRequest(object):
    print("DO SYNC REQUEST")
    global groups
    #检查并行任务数量
    if len(groups) == MAXGROUPCOUNT:
        print("达到最大数量")
        return
    
    #groups.append(object)

    global batch


    url = 'https://vivago.ai/api/gw/v2/video/video_diffusion/async'
    global cookie_g
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiI3YjU2MjM0ZC0yZDQxLTQzZjEtYjg4MC1hNWNkNTQ3ZGQzZjQiLCJ1c2VybmFtZSI6Imdvb2dsZV9FalN4b0dPIiwicGhvbmVudW0iOiIxMjM0NTY3ODkxMCIsImVtYWlsIjoid2FuZ3poYW95dW54MzNAZ21haWwuY29tIiwicm9sZSI6ImFwaSZlLWNvbW1lcmNlciZnZW5lcmFsJndlbnlpbiIsImV4cCI6MTcyMTgwMDYwNX0.WDU6Fsp3zj1st_GaNu4OC3wRhtqUqjkeNzn4z3APUZE'
    cookie = cookie_g
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        'Cookie' : cookie,
        'User-Agent' : user_agent
    }

    #path = object.imagepath
    imagebase64 = tool.getImageBase64Code(object)

    request_id = tool.getUuid()
    #object.request_id = request_id


    #print(f"{object.imagepath}___DID  STORE CHANGE ? AFTER = {object.request_id}")

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

    #print(f"in doSyncRequest ----Code = {response.status_code},result = {result}")
    resultDic = json.loads(result)
    taskid = resultDic['result']['task_id']
    global currentTaskId
    currentTaskId = taskid

    print(f"taskid = {taskid}")
    doResultRequest(taskid)

def doResultRequest(taskid):
    print("DO RESULT REQUSET")
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

    #print(f" in doResultRequest ------Code = {response.status_code},result = {result}")

    if response.status_code == 200:

        global batch
        if len(batch) < MAXGROUPCOUNT:
            batch.append(taskid)
            if len(batch) == MAXGROUPCOUNT:
                doBatchesRequest()   
            else:
                doGroup(path)
        #doBatchRequest(taskid)

def doBatchesRequest():
    global batch
    print(f"DO BATCH REQUEST WITH TASK ID LIST : {batch}")
    global currentTaskId
    global batchCallBack

    
    #if taskid == "" and currentTaskId != "":
        #taskid = currentTaskId

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
        'task_id_list' : batch
    }

    response = requests.post(url,json=data,headers=headers)
    result = response.content.decode("utf-8")
    #print(f"in doBatchesRequest RESULT = {result}")
    resultDic = json.loads(result)
    sub_task_results = resultDic['result']

    global bool_ShouldStopAfer
    #print("ENTER FOR LOOP")
    finishOne = False
    finishSub = None
    for batch_taskid in batch:
        #print(f"CHOOSEN TASK ID = {batch_taskid}")
        for sub in sub_task_results:
            current = sub['task_id']
            if current == batch_taskid:
                completion = sub['sub_task_results'][0]['task_completion']
                print(f"TASK {current} WITH COMPLETION {completion}")
                if completion == 1:
                    finishOne = True
                    finishSub = sub
                    break
                else:
                    bool_ShouldStopAfer = True

        #break

    if finishOne and finishSub:

        bool_ShouldStopAfer = False

        global rootafter_id
        if rootafter_id != "":
            print(f"CANCEL ROOT AFTER with id {rootafter_id}")
            #root.after_cancel(rootafter_id)

        vedioname = finishSub['sub_task_results'][0]['video']
        d_id = finishSub['task_id']
        doDownload(vedioname,d_id)
    else:
        print("BEFORE ROOT AFTER")            
        rootAfterCallBack()
        
def StartNewBatch(taskid):
    print(f"START NEW BATCH WITH REMOVE TASKID:{taskid}")
    global batch
    index = batch.index(taskid)
    batch.pop(index)
    doGroup(path)

def doBatchRequest(taskids):
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
        'task_id_list' : taskids
    }

    response = requests.post(url,json=data,headers=headers)
    result = response.content.decode("utf-8")

    #print(f"in doBatchRequest Code = {response.status_code},result = {result}")

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



def doDownload(filename,taskid):
    print("DO DOWNLOAD")
    global downloadTargetPath,index,downloadIndex
    url = 'https://media.vivago.ai/' + filename
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    headers = {
        'User-Agent' : user_agent
    }

    response = requests.get(url,headers=headers,stream=True)
    if response.status_code == 200:
        if not os.path.exists(downloadTargetPath):
            os.makedirs(downloadTargetPath)
        prefix = ""
        if downloadIndex < 10:
            prefix = '00' + str(downloadIndex)
        elif downloadIndex < 100:
            prefix = '0' + str(downloadIndex)
        else:
            prefix = ""
        downloadIndex += 1

        targetpath = downloadTargetPath + '/' + prefix + '_' + filename
        # 以二进制模式打开文件（写模式）
        with open(targetpath, 'wb') as file:
            # 写入文件（可以分块写入以节省内存）
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
            StartNewBatch(taskid)
            #global taskFinishCallback
            #if taskFinishCallback:
                #taskFinishCallback(True)
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
    
    global path
    path = os.path.dirname(imagePath)
    doGroup(path)

def doGroup(path):
    print("DO GROUP")
    global groups,index
    print(f"Path = {path}")
    pg_files = glob.glob(os.path.join(path, '*.jpg'))
    global index
    if index < len(pg_files):
        file = pg_files[index]
        print(f"GET IMAGE IN {file} WITH INDEX {index}")
        data = ViviaObject(request_id="",imagepath=file,index=index)
        #doThreadRquest(file)
        index += 1
        doSyncRequest(file)
    else:
        print("END")

        global batch
        if len(batch) > 0:
            global bool_ShouldStopAfer
            bool_ShouldStopAfer = True
            rootAfterCallBack()
        else:
            if taskFinishCallback:
                taskFinishCallback(True)
        

def doThreadRquest(data):
    
    #file = data.imagepath
    print(f"DATA = {data}")
    thread = threading.Thread(target=doSyncRequest,args=(data))
    thread.start()


def rootAfterCallBack():
    print("ENTER ROOT AFTER")
    global bool_ShouldStopAfer
    global rootafter_id
    if bool_ShouldStopAfer:
        print("DO ROOT AFTER")

        if batchCallBack:
            batchCallBack()

        #after_id = root.after(10000,lambda: doBatchesRequest())
        #rootafter_id = str(after_id)
        #print(f"ROOT ID  = {after_id}")
    

#root.mainloop()