import requests
import shutil
import base64
import os

filePath = ""

def download_image(url, path,name,callback):

    customPrint("WILL DOWNLOAD" + url )
    combinedUrl = url + "\n"

    file_path = "E:/hero/3/imageUrls.txt"
    with open(file_path,"a") as file:
        file.write(combinedUrl)
        callback(name)

def configFilePath(choosenPath):
    global filePath

    filePath = choosenPath
    os.makedirs(filePath)

def base2img(base64Code,filename):
    customPrint("GET BASE64")

    global filePath
    if filePath == "":
        customPrint("INVALID FILEPATH")
    else:
        imageData = base64.b64decode(base64Code)
        image_name = str(filename)
        file_path = filePath + "/" + image_name + ".png"
        customPrint(f"WILL DOWNLOAD at {file_path}" )
        with open(file_path,"wb") as file:
            file.write(imageData)

def img2base(image_path):
    with open(image_path,"rb") as imageFile:
        encodeStr = base64.b64encode(imageFile.read())
    return encodeStr

def customPrint(content):
    print("\n" + content + "\n")

def log(content):
    print("\n" + content + "\n")
    

