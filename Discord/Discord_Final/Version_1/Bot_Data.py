import enum
from enum import Enum

class DataType(Enum):
    DEFAULT = "86"
    SESSION_ID = "123"
    PROGRESS = "0"

class DataFromBot:

    def __init__(self, type : DataType, data : str):
            self.type = type
            self.data = data

    def __str__(self):
            return f"type = {self.type} and Data = {self.data}."