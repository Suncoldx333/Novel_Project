import enum
from enum import Enum

class DataType(Enum):
    DEFAULT = "86"
    SESSION_ID = "123"
    PROGRESS = "0"
    IMAGEURL = "1231"
    CUSTOMID = {}

class DataFromBot:

    def __init__(self, type : DataType, data : str):
            self.type = type
            self.data = data

    def __str__(self):
            return f"type = {self.type} and Data = {self.data}."
    
class CustomIdObject:
    def __init__(self, type : DataType, messageId : str, guildId : str,channelId : str,customIds : str):
            self.type = type
            self.messageId = messageId
            self.guildId = guildId
            self.channelId = channelId
            self.customIds = customIds

    def __str__(self):
            return f"messageID = {self.messageId} and guildId = {self.guildId} and channelId = {self.channelId}."
    
class ImageUrlObject:

    def __init__(self, type : DataType, url : str):
            self.type = type
            self.url = url

    def __str__(self):
            return f"type = {self.type} and Url = {self.url}."

class ViviaObject:

    def __init__(self, request_id : str, imagepath : str, index : int):
            self.request_id = request_id
            self.imagepath = imagepath
            self.index = index

    def __str__(self):
            return f"imagepath = {self.imagepath} and request_id = {self.request_id} and index = {str(self.index)}."