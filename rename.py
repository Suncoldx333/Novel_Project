import os

def contains_parent(s):
    if "()" in s or ")" in s:
        return True
    else:
        return False

def getnum(s):
    return "".join([c for c in s if c.isdigit()])

def batch_rename_files(folder_path, prefix, withHead):
    # 获取文件夹内所有文件名
    files = os.listdir(folder_path)
    
    # 遍历文件夹内所有文件
    for file_name in files:
        # 构造新的文件名
        '''       
        if contains_parent(file_name):
            print(f"文件名修改前={file_name}")
            number = int(getnum(file_name))

            if withHead:
                number = int((number - 4) / 10) + 1
                numberStr = str(number)
                new_file_name = prefix + numberStr
                new_file_name = new_file_name + ".mp4"
            else:
                number = int((number - 4) / 10) + 0
                numberStr = str(number)
                new_file_name = prefix + numberStr
                new_file_name = new_file_name + ".mp4"
        else:
            new_file_name = prefix + "1.mp4"
        '''
        
        new_file_name = prefix + file_name
        
        # 构造文件的完整路径
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f"{old_file_path} -> {new_file_path}")

# 调用函数批量修改文件名,True表示有第0号视频
batch_rename_files("E:\新建文件夹\十年寒窗", "短剧", False)
