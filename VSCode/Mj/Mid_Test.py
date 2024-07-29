import requests
import json
import time

import base64
import cv2
import numpy as np

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
'''
ttid = "1715775133377489"
ccid = "MJ::JOB::upsample::1::1fd87706-a4f1-4204-a916-721374e31842"
action(ttid,ccid)
'''
image2base64()