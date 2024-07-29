import json
import os

file_path = "D:/novel/array.txt"

def test():

    dicArray = []

    if os.path.exists(file_path) and file_path.endswith('.txt'):
        with open(file_path,'r',encoding='UTF-8') as file:
            content = file.read()
            #print("novel = " + content)
            sep = '\\n\\n'
            #sd = json.loads(content)

            array = content.split(sep)
            for item in array:
                #print(item + "~~~~~~")

                sep2 = '\\n'
                array2 = item.split(sep2)
                dic = {}
                for index,value in enumerate(array2):
                    
                    if "分镜" in value:
                        dic['screen'] = extract_strings(value,"：","。")
                    elif "画面描述" in value:
                        dic['CN'] = extract_strings(value,"：","。")
                    elif "英文描述" in value:
                        dic['EN'] = extract_strings(value,"：",".")
                dicArray.append(dic)
            print(dicArray)
    else:
        print("fail")
    return dicArray

def extract_strings(text,head,end):
    result = []
    start_index = 0
    while True:
        start = text.find(head, start_index)
        if start == -1:
            break
        end = text.find(end, start + 1)
        if end!= -1:
            result.append(text[start + 1 : end + 1])
        start_index = start + 1
    return result

def find_bracketed_strings(text):
    #print("begin------" + text)
    results = []
    start_index = 0
    while True:
        start = text.find('[', start_index)
        #print("start = " + str(start))
        if start == -1:
            break
        end = text.find(']', start + 1)
        #print("end = " + str(end))
        if end!= -1:
            results.append(text[start:end + 1])
            #print("result = " + text[start:end + 1])
        start_index = end + 1
    return results

def find(allStr):

    

    return json.loads(allStr)

    '''
    head = "English: "
    end = "."
    
    mainstr = ""

    array = find_bracketed_strings(allStr)
    #print("array = " + array)
    if len(array) == 1:
        mainstr = array[0]
       # print(mainstr)
        return seprate(mainstr)
    else:
        count = array.count
        print("fail with count : " + str(count))
        return ["Fail"]
    #mainstr = "画面描述：镜头逐渐拉远，陈伶面对神秘发现，散发出一种神秘的光芒。\n    英文描述：The camera gradually zooms out as Chen Ling faces the mysterious discovery, emanating a mystical glow"
    #mainstr = allStr
def seprate(str):
    #print("str = " + str)
    mainss = ""
    str = "[\"Chen Ling sneezed in the cold wind, bathed in sunlight.\",\n\"The wheels of the cart rolled as the boy scattered salt on the road, melting the frost slowly.\",\n\"Zhao Yi taunted Chen Ling, intending to provoke a confrontation.\"]"
    if '\n' in str:
        print("yes")
    else:
        print("no")
    strs = str.split('\n')

    sdarray = json.loads(str)
    for sd in sdarray:
        print(sd)

    
    cuts = []



    for simstr in strs:
        print(simstr+"---finish---")
        #appstr = '"' + str + '"'
        sep = '\"'
        
        index = simstr.find(sep)
        l = len(sep)

        index2 = index + 1
        

        index_end = simstr.find(".") + 1
        cutend = simstr[index2 : index_end]

        cuts.append(cutend)
        #print(cutend)
       # print(cuts)
        cut_str = json.dumps(cuts)   #数组转json

        array = json.loads(cut_str)

        print(cut_str + "---loop")

    #return cut_str    
    '''

