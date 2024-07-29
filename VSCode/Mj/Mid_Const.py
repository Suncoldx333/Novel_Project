import requests
import shutil

def download_image(url, path,name,callback):

    customPrint("WILL DOWNLOAD" + url )
    combinedUrl = url + "\n"

    file_path = "E:/hero/3/imageUrls.txt"
    with open(file_path,"a") as file:
        file.write(combinedUrl)
        callback(name)

'''
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print(f"无法下载图片，状态码: {response.status_code}")
'''
def customPrint(content):
    print("\n" + content + "\n")

def log(content):
    print("\n" + content + "\n")
    

