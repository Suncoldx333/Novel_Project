import requests
import shutil
import os

def download_image(url, path,name,callback):

    customPrint("WILL DOWNLOAD" + url )
    #combinedUrl = url + "\n"

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        callback(True,name)
    else:
        print(f"无法下载图片，状态码: {response.status_code}")
        callback(False,name)

def customPrint(content):
    print("\n" + content + "\n")

def log(content):
    print("\n" + content + "\n")

def configFilePath(choosenPath):
    global filePath

    filePath = choosenPath
    os.makedirs(filePath)

