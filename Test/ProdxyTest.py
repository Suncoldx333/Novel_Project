import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 时间格式
    filename='app.log',  # 日志文件名
    filemode='w'  # 文件模式，'w'表示每次运行都会清空日志文件重新写入
)

# 创建一个logger实例
logger = logging.getLogger(__name__)

def main():
    logger.info('程序开始执行')  # 记录一条信息日志
    # 模拟程序执行过程
    result = perform_operation()
    logger.info(f'操作结果: {result}')  # 记录操作结果
    logger.info('程序执行结束')

def perform_operation():
    # 示例操作，这里简单返回一个字符串
    return "操作成功"

if __name__ == '__main__':
    main()