class MyClass:
    def __init__(self, name, value):
        # 初始化方法
        self.name = name
        self.value = value

    def __repr__(self):
        return f"MyClass(name={self.name}, value={self.value})"

    def display_info(self):
        print(f"Name: {self.name}, Value: {self.value}")

# 创建类的实例
obj = MyClass("example", 123)

# 打印对象
print(obj)

# 调用类的方法
obj.display_info()
