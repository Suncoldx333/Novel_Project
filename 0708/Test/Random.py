import uuid
import os
import glob

# 生成一个随机的UUID
def test():
    path = 'E:/hero/0717/shangyang/Images_test/Downloads'
    jpg_files = glob.glob(os.path.join(path, '*.jpg'))
    print(f"Count = {str(len(jpg_files))}")
    files = os.listdir(path)
    for file in files:
        path_i = os.path.join(path,file)
        print(f"PATH = {path_i}")



test()