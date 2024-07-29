import requests
import os

def fetchbetween(path,targetPath):
    with open (path,'r',encoding='UTF-8') as file:
        content = file.read()
        #contents = content.split('\n')
        query = extract_hash_content(content)
        #for text in contents:
            #start_index = text.find('#', 0)
            #query = extract_hash_content(text)

    if len(query) > 0:
        for index, promt in enumerate(query):
            print(promt)
            if index < len(query):
                line = promt + '\n'
            else:
                line = promt
            with open(targetPath,'a') as file :
                file.write(line)
        

def extract_hash_content(s):
    result = []
    start_index = 0
    
    # 寻找所有的 # 开头的位置
    while True:
        start_index = s.find('$', start_index)
        if start_index == -1:  # 如果找不到 # 则退出循环
            break
        
        end_index = s.find('$', start_index + 1)  # 寻找下一个 #
        if end_index == -1:  # 如果找不到第二个 # 则退出循环
            break
        
        # 提取 # 和 # 之间的内容
        hash_content = s[start_index + 1 : end_index]
        result.append(hash_content)
        
        start_index = end_index + 1  # 更新开始位置为上一个 # 之后的一个字符
    
    return result

#def askGpt(hero_name):

path = 'E:/hero/0728_2/zengzi/all.txt'
target = 'E:/hero/0728_2/zengzi/prompt.txt'

fetchbetween(path,target)