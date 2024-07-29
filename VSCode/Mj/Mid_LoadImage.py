import requests
import shutil

import os

import Mid_Const as Const

def calculateScale():
    
    imageUrls = "E:/hero/3/imageUrls.txt"
    prefix = "E:/hero/3/Images/"

    bool_prompt = os.path.exists(imageUrls) and imageUrls.endswith('.txt')

    if bool_prompt:
        with open(imageUrls,'r',encoding='UTF-8') as file:
            content = file.read()
            print("content = " + content)
            images = content.split('\n')

            for index,item in enumerate(images):
                Const.log(item)
                name = "Image" + str(index) + ".jpg"
                Const.log(name)
                file_path = prefix + name
                Const.log(file_path)
                #jdownload_image(item,file_path)


def download_image(url, file_path):
    print("开始下载")
    response = requests.get(url)
    if response.status_code == 200:
        print("下载成功")
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"下载失败，状态码: {response.status_code}")
                

#calculateScale()