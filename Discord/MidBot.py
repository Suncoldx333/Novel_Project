import requests

def qwe():
    url = "https://jsonplaceholder.typicode.com/users/1/todos"
    response = requests.get(url)

    if response.status_code == 200:
        todos = response.json()
        print(response.status_code)
    else:
        print(f"请求失败，状态码：{response.status_code}")
qwe()