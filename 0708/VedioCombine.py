from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

from tkinter import filedialog,Tk,Button
from tkinter.filedialog import askopenfilename
import glob

root = Tk()
windowWidth = 300
windowHeight = 240
targetWidth = 1760
targetHeight = 990

root.geometry(f"{windowWidth}x{windowHeight}+600+50")


button_bot = Button(root,text="Pic2Vedio",command=lambda: createVediofromImages())
button_bot.pack()

def createVediofromImages():
    global targetWidth,targetHeight

    imageFilePaths = []

    folder_path = filedialog.askdirectory()
    targetpath = folder_path + '\combine.mkv'
    if folder_path:
        jpg_files = glob.glob(folder_path + '**/*.mp4', recursive=True)
        vedioclips = []
        for index,video_path in enumerate(jpg_files):
            vedioclip = VideoFileClip(video_path)
            startTime = index * 3
            if index == 0:
                fade = vedioclip.fx(fadeout, 1).set_start(startTime)
                vedioclips.append(fade)
            else:
                fade = vedioclip.set_start(startTime).crossfadein(1).fx(fadeout, 1)
                vedioclips.append(fade)
        
        final_video = CompositeVideoClip(vedioclips)

    # 保存最终合成的视频为MKV格式
        final_video.write_videofile(targetpath, fps=24, codec="libx264")

    '''
        global video_a_path,video_b_path
        video_a_path = jpg_files[0]
        video_b_path = jpg_files[1]
        video_c_path = jpg_files[2]
    # 加载视频剪辑
    video_a = VideoFileClip(video_a_path)
    video_b = VideoFileClip(video_b_path)
    vidwo_c = VideoFileClip(video_c_path)
    # 在视频A的最后1秒逐渐淡出
    video_a_faded = video_a.fx(fadeout, 1).set_start(0)

    # 视频B在第3秒透明度从0逐渐变为100
    video_b_start = video_b.set_start(3).crossfadein(1).fx(fadeout, 1)

    video_c_start = vidwo_c.set_start(6).crossfadein(1).fx(fadeout, 1)

    # 合成视频，将带有淡出效果的视频A和渐变的视频B叠加
    final_video = CompositeVideoClip([video_a_faded, video_b_start,video_c_start])

    # 保存最终合成的视频为MKV格式
    final_video.write_videofile("E:/hero/mengzi-0705\Vedios\combine8.mkv", fps=24, codec="libx264")

    # 保存最终合成的视频
    #final_video.write_videofile("E:/hero/mengzi-0705\Vedios\combine6.mp4", fps=24, codec="libx264", alpha=True)
'''
root.mainloop()
