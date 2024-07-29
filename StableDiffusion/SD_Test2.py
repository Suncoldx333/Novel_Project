import time
import multiprocessing

def child_process(queue):
    # 子进程执行的任务
    result = "Data from child process"
    # 将结果放入队列
    queue.put(result)

def main():
    # 创建队列
    queue = multiprocessing.Queue()
    
    # 创建子进程
    p = multiprocessing.Process(target=child_process, args=(queue,))
    p.start()
    
    # 轮询队列，检查是否有新数据
    while True:
        if not queue.empty():
            # 如果队列非空，则读取数据
            data = queue.get()
            print(f"Received data: {data}")
            break
        else:
            # 队列为空，短暂休眠后再次检查
            time.sleep(0.1)
    
    # 等待子进程结束
    p.join()
    
    print("Child process finished.")

if __name__ == '__main__':
    main()