import requests
import shutil
import base64

def download_image(url, path,name,callback):

    customPrint("WILL DOWNLOAD" + url )
    combinedUrl = url + "\n"

    file_path = "E:/hero/3/imageUrls.txt"
    with open(file_path,"a") as file:
        file.write(combinedUrl)
        callback(name)

def base2img(base64Code,filename):
    customPrint("GET BASE64")

    imageData = base64.b64decode(base64Code)
    image_name = str(filename)
    file_path = "E:/novel_ai/" + image_name + ".png"
    with open(file_path,"wb") as file:
        file.write(imageData)


def customPrint(content):
    print("\n" + content + "\n")

def log(content):
    print("\n" + content + "\n")
    

