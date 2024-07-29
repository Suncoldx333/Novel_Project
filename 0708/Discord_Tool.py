from datetime import datetime
import base64
import uuid

def getTimeStampe():
    current_timestamp = datetime.now().timestamp()
    return int(current_timestamp)

def getImageBase64Code(imagePath):
    with open(imagePath, "rb") as img_file:
        # 使用base64标准库进行编码
        encoded_string = base64.b64encode(img_file.read())
    
    # 将bytes类型的数据解码为字符串
    return encoded_string.decode('utf-8')

def getUuid():
    key = str(uuid.uuid4())
    return key