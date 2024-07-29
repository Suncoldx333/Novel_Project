from moviepy.editor import ImageClip,concatenate_videoclips,ColorClip
import os
import glob
from tkinter import filedialog,Tk,Button
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
from moviepy.video.fx import resize

root = Tk()
windowWidth = 300
windowHeight = 240
targetWidth = 1760
targetHeight = 990

keyframes = None

root.geometry(f"{windowWidth}x{windowHeight}+600+50")

button_bot = Button(root,text="Pic2Vedio",command=lambda: createVediofromImages())
button_bot.pack()

def createVediofromImages():
    global targetWidth,targetHeight

    imageFilePaths = []

    folder_path = filedialog.askdirectory()
    if folder_path:
        # 使用 glob 模块递归查找所有 .jpg 文件
        jpg_files = glob.glob(folder_path + '**/*.mp4', recursive=True)

        # 打印找到的 .jpg 文件路径
        for file_path in jpg_files:
            print(file_path)
            imageFilePaths.append(file_path)
        #print(f"COUNT = {len(imageFilePaths)}")

    return
    original_size = (640, 480)  # 原始视频尺寸
    video_duration = 4  # 视频总时长 4 秒
    background_clip = ColorClip(size=original_size, color=(0, 0, 0))
    background_clip = background_clip.set_duration(video_duration)

    imageClips = [background_clip]

    if len(imageFilePaths) > 0 :
        for path in imageFilePaths:
            clip = ImageClip(path,duration=4)
            #resized = clip.resize(1.1)
            clip_re = resize.resize(clip=clip,newsize=0.5)
            
            global keyframes
           # keyframes = calculate(clip.w,clip.h)
            #positioned = resized.set_position(interpolate_position)

            imageClips.append(clip_re)
            break
    
    final = concatenate_videoclips(imageClips)
    outputpath = folder_path + "/final.mp4"
    final.write_videofile(outputpath, fps=24)

def calculate(image_w,imagee_h):
    dis_w = image_w * 0.05
    dis_h = imagee_h * 0.05

    n_dis_w = -1 * dis_w
    n_dis_h = -1 * dis_h

    keyframes = [(0,(n_dis_w,n_dis_h)),(2,(n_dis_w,n_dis_h / 2)),(4,(n_dis_w,0))]
    return keyframes



# 定义关键帧位置
#keyframes = [(0, (100, 100)), (2, (500, 500)), (4, (300, 300))]

# 定义位置函数，使用线性插值
def interpolate_position(t):
    global keyframes
    for i in range(len(keyframes)-1):
        if keyframes[i][0] <= t < keyframes[i+1][0]:
            t1, pos1 = keyframes[i]
            t2, pos2 = keyframes[i+1]
            alpha = (t - t1) / (t2 - t1)
            x = int(np.interp(t, [t1, t2], [pos1[0], pos2[0]]))
            y = int(np.interp(t, [t1, t2], [pos1[1], pos2[1]]))
            return (x, y)
    return keyframes[-1][1]  # 返回最后一个关键帧的位置

root.mainloop()


