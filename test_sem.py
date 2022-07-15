# **coding: utf-8**
import threading
import time


def hello(n, sema):
    sema.acquire()
    print('调用线程　{0}'.format(n))
    sema.release()


# 信号量管理表示realse()调用数减去acquire()调用数加上去一个初始值的计数器　　1　-　5　+　0　＝　-4　
sema = threading.Semaphore(value=0)
workers = 5
for n in range(workers):
    t = threading.Thread(target=hello, args=(n + 2, sema,))
    t.start()

time.sleep(3)
print('开启线程')
sema.release()