import multiprocessing
import threading
import time

def child_process(queue):
    for i in range(5):
        message = f"Message {i} from child process"
        queue.put(message)
        print(f"Child process sent: {message}")
        time.sleep(1)  # 模拟子进程工作

def thread_function(queue):
    while True:
        if not queue.empty():
            message = queue.get()
            print(f"Thread received: {message}")
            if message == "Message 4 from child process":
                break  # 收到特定消息后退出
        else:
            print("Thread: No data yet.")
        time.sleep(0.5)  # 短暂等待

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    # 创建子进程
    p = multiprocessing.Process(target=child_process, args=(queue,))
    p.start()

    # 创建新线程
    t = threading.Thread(target=thread_function, args=(queue,))
    t.start()

    # 等待子进程结束
    p.join()

    # 等待线程结束
    t.join()

    print("Main thread: All done.")
