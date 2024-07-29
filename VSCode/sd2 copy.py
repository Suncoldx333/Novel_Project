import json
json_string = '{"name" : "张三"}'
data_dict = json.loads(json_string)
print(data_dict)

value = data_dict['name']
print(value)