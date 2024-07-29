import os
import glob
import requests
import shutil

ImageUrls = []
index = 0
filepath = ""

download_Callback = None
download_folder = ""

def read_txt_files(directory):
    # 使用glob递归地查找所有.txt文件
    txt_files = glob.glob(os.path.join(directory, '**', '*.txt'), recursive=True)
    
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            yield file_path, content

def download_image(url, folder_path, file_name, callback):
    global filepath
    filepath = folder_path
    print(f"FILE PATH~~~~~~ = {folder_path}")
    try:
        # 检查文件夹是否存在，如果不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # 构建完整的文件路径
            #file_path = os.path.join(folder_path, file_name)
            file_path = folder_path  + "/" + file_name + ".jpg"
            # 以二进制写入方式打开文件，并写入图片数据
            print(f"FILE PATH = {file_path}")
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                print(f"Image successfully downloaded: {file_path}")
                callback(True,file_name,file_path)
            
            
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            callback(False,file_name)
        
    except PermissionError as e:
        print(f"Permission denied: {e}")
        callback(False,file_name,file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        callback(False,file_name,file_path)

def Download():
    global ImageUrls
    global index
    global download_folder
    directory = download_folder  # 主目录名称
    directory = 'E:/hero/0717/gongsunlong/Images/Downloads'
    if index == len(ImageUrls):
        global download_Callback
        if download_Callback:
            download_Callback(download_folder)
        return
    else:
        content = ImageUrls[index]
        download_image(content,directory,str(index),downloadCallback)

def downloadCallback(Success,name,path):
    global index
    index += 1
    Download()

def OutterDownload(folder_path,download_folder_path,callback):
    global ImageUrls
    global download_folder
    global download_Callback
    download_Callback = callback
    download_folder = download_folder_path

    for file_path, content in read_txt_files(folder_path):
        ImageUrls.append(content)
    Download()


def main():
    directory = 'E:/hero/0717/gongsunlong/Images'  # 主目录名称
    imageDownPath = '/Download'
    global ImageUrls
    for file_path, content in read_txt_files(directory):
        #print(f"File: {file_path}")
        #print(f"Content: {content}")
        #print("-" * 5)
        ImageUrls.append(content)
    Download()

if __name__ == "__main__":
   main()
