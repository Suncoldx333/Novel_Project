import requests
import pyautogui


def test():

    indexs = [1,2,3]
    for index in indexs:
        print(str(index))
        file_path = "E:/hero/outside/imageUrls_Test.txt"
        combinedUrl = str(index) + "\n"
        with open(file_path,"a") as file:
            file.write(combinedUrl)

    

def download_image(url, file_path):
    print("开始下载")
    response = requests.get(url)
    if response.status_code == 200:
        print("下载成功")
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"下载失败，状态码: {response.status_code}")

# 要下载的图片 URL
image_url = "https://mjimg.open-hk.com/attachments/1244870718056038424/1244917877325434890/riafletunweixcom_Ink_Wash_Painting_StyleCold_lightBeneath_the_s_85f4be1d-3b7a-4462-bdda-5fa909f094aa.png?ex=6656db9f&is=66558a1f&hm=1357e1f163298945145081dcff17a0d891a429b20e25a8a4daf3236548a37199&"
# 保存图片的路径
save_path = "E:/hero/outside/image_download14.jpg"

#download_image(image_url, save_path)
#test()