import requests
import json

url = "https://api.openai-hk.com/v1/chat/completions"

ques = "你是chatGPT多少？"

def translate(des):
    ques = des + "------请将这段文字翻译成英文"
    print("ques = " + ques)
    des = ask(ques)
    return des

def makehero():
    ques = "根据伍子胥所在的时代背景，描写伍子胥的人物形象,对外貌进行详细描写"
    print("ques = " + ques)
    des = ask(ques)
    return des

def askscreens():
    ques = "请为每个分镜创作画面描述，要求简洁，可以提供给midjourney进行文生图"
    ask(ques)

def ask(ques):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
        }

    data = {
        "max_tokens": 1200,
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "top_p": 1,
        "presence_penalty": 1,
        "messages": [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
            },
            {
                "role": "user",
                "content": ques
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    dicData = json.loads(result)
    choice = dicData['choices']
    first = choice[0]
    message = first['message']
    content = message['content']

    print(result)
    return content

def makescreen(novel):

    if len(novel) == 0:
        print ("empty novel")
        return "empty";
    else:
        global ques
        ques = novel + "以白起人物解说为主题，写一个具有传奇色彩和反差感的人物传记故事脚本，一共涵盖10个分镜,并为每个分镜创作简洁的画面描述,同时将每个画面描述翻译成英，最后将分镜与英文的画面描述合并为列表返回"

        headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
        }

        data = {
            "max_tokens": 1200,
            "model": "gpt-3.5-turbo",
            "temperature": 0.8,
            "top_p": 1,
            "presence_penalty": 1,
            "messages": [
                {
                    "role": "system",
                    "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
                },
                {
                    "role": "user",
                    "content": ques
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
        result = response.content.decode("utf-8")
        dicData = json.loads(result)
        choice = dicData['choices']
        first = choice[0]
        message = first['message']
        content = message['content']

        print(result)
        return content



def makemore(command):


    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer hk-vioogw10000222966d3e728fa0117826984e2b39e338a43d"
    }

    data = {
        "max_tokens": 1200,
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "top_p": 1,
        "presence_penalty": 1,
        "messages": [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8') )
    result = response.content.decode("utf-8")
    dicData = json.loads(result)
    choice = dicData['choices']
    first = choice[0]
    message = first['message']
    content = message['content']


    print(result)
    return content
    

