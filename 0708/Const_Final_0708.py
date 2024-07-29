import requests
import shutil
import os

filePath = ""

def writeImageUrl(url, folder_path, file_name, callback):

    global filePath
    folder_path = filePath
    print(f"FILE PATH~~~~~~ = {folder_path}")
    try:
        # 检查文件夹是否存在，如果不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = folder_path  + "/" + file_name + ".txt"
        with open(file_path, 'w', encoding='utf-8') as file:
            # 写入字符串
            file.write(url)
        callback(True,file_name,file_path)

        # 获取图片数据
        '''
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # 构建完整的文件路径
            #file_path = os.path.join(folder_path, file_name)
            file_path = folder_path  + "/" + file_name + ".jpg"
            # 以二进制写入方式打开文件，并写入图片数据
            print(f"FILE PATH = {file_path}")
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                callback(True,file_name,file_path)
            print(f"Image successfully downloaded: {file_path}")
            
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            callback(False,file_name)
        '''
    except PermissionError as e:
        print(f"Permission denied: {e}")
        callback(False,file_name,file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        callback(False,file_name,file_path)




def download_image2(url, path,name,callback):

    customPrint("WILL DOWNLOAD == " + url )
    #combinedUrl = url + "\n"
    global filePath
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(filePath, 'wb') as out_file:
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
    print(f"CONFIG PATH = {filePath}")
    if os.path.exists(filePath):
        print(f"EXIST : {filePath}")
    else:
        print(f"MAKE FILE : {filePath}")
        os.makedirs(filePath)

