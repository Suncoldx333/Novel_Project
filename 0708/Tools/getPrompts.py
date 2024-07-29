import re
import os

def extract_english_words(text):
    # 使用正则表达式匹配所有连续的英文字符，包括连字符和撇号
    pattern = r'[A-Za-z\,\.\s-]+'
    pattern2 = r'\b[a-zA-Z]+(?:\s*[,\.\']?[ \t]*[a-zA-Z]+)*(?:\s*[,\.])?\b'
    english_words = re.findall(pattern2, text)
    return english_words

# 示例文本，包含连字符和撇号
text = "在'this'字符串中有许多混合的单词，如well-known, don't以及high-quality。"

import re

def contains_english(s):
    return bool(re.search('[a-zA-Z]', s))

def fetpromtps():
    folder_path = 'E:/hero/0728/dengqi/all.txt'
    target_path = 'E:/hero/0728/dengqi/Prompts.txt'
    with open(folder_path,'r',encoding='UTF-8') as file:
        content = file.read()
        contents = content.split('\n')
        for line in contents:
            #print(f"line = {line}")
            if contains_english(line):
                cut = extract_english_words(line)
                out = 'English Description'
                if out in cut:
                    asd = len(out)
                else:
                    
                    if isinstance(cut,list):
                        fetch = cut[0]
                        more = fetch + '\n'
                        print(f"cut = {fetch}")
                        with open(target_path,'a',encoding='utf-8') as file:
                            file.write(more)
        with open(target_path,'r',encoding='utf-8') as file:
            files = file.read()
            if files:
                cutfile = files[:-1]

                with open(target_path,'w',encoding='utf-8') as file:
                    file.write(cutfile)

                with open(target_path,'r',encoding='utf-8') as file:
                    files = file.read()
                    array = files.split('\n')
                    print(f"COUNT = {len(array)}")

        

# 调用函数
#result = extract_english_words(text)

# 输出结果
#print(result)  # 输出: ["'this'", 'well-known', "don't", 'high-quality']
fetpromtps()