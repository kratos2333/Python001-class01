# 第三周 学习笔记
## 并发参数优化
``` 
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
```

## twisted 异步IO框架
## 多进程
https://docs.python.org/zh-cn/3.7/library/multiprocessing.html#the-process-class
### 进程的创建和运行
#### multiprocessing 基本参数
``` 
# 参数
# multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})

# - group：分组，实际上很少使用
# - target：表示调用对象，你可以传入方法的名字
# - name：别名，相当于给这个进程取一个名字
# - args：表示被调用对象的位置参数元组，比如target是函数a，他有两个参数m，n，那么args就传入(m, n)即可
# - kwargs：表示调用对象的字典

from multiprocessing import Process

def f(name):
    print(f'hello {name}')

if __name__ == '__main__':
    p = Process(target=f, args=('john',))
    p.start()
    p.join()
# join([timeout])
# 如果可选参数 timeout 是 None （默认值），则该方法将阻塞，
# 直到调用 join() 方法的进程终止。如果 timeout 是一个正数，
# 它最多会阻塞 timeout 秒。
# 请注意，如果进程终止或方法超时，则该方法返回 None 。
# 检查进程的 exitcode 以确定它是否终止。
# 一个进程可以合并多次。
# 进程无法并入自身，因为这会导致死锁。
# 尝试在启动进程之前合并进程是错误的。
```
#### 注意
windows创建多进程，必须在if __name__ == '__main__'中创建

#### 输出一些关于进程的信息
multiprocessing.active_children() --- check number of active child process
multiprocessing.cpu_count() --- check how many cpu so you can create the number of processes
os.cpu_count() -- in the multiprocessing/context.py BaseContext class, multiprocessing.cpu_cout() call os.cpu_count()
os.getppid() -- get parent processid
os.getpid() -- get processid

``` 
# 显示所涉及的各个进程ID，这是一个扩展示例

from multiprocessing import Process
import os
import multiprocessing

def debug_info(title):
    print('-'*20)
    print(title)
    print('模块名称:', __name__)
    print('父进程:', os.getppid())
    print('当前进程:', os.getpid())
    print('-'*20)

def f(name):
    debug_info('function f')
    print('hello', name)

if __name__ == '__main__':
    debug_info('main')
    p = Process(target=f, args=('bob',), name="child-1")
    p.start()

    for p in multiprocessing.active_children():
        print(f'子进程名称: {p.name}  id: { str(p.pid) }' )
    print('进程结束')
    print(f'CPU核心数量: { str(multiprocessing.cpu_count()) }')
    
    p.join()
``` 
#### 用面向对象的方式创建进程
当不给Process指定target时，会默认调用Process类里的run()方法。
这和指定target效果是一样的，只是将函数封装进类之后便于理解和调用。
```
from multiprocessing import Process
import os
class MyProcess(Process):
    def __init__(self,name):
        self.name = name
        super().__init__()

    def run(self):
        print(f'i am process {self.name}, my processId is {os.getpid()}, my parent is {os.getppid()}')

for i in range(3):
    p = MyProcess('process'+str(i))
    p.start()
```

### 进程间的通信
https://docs.python.org/zh-cn/3.7/library/multiprocessing.html#exchanging-objects-between-processes
可以通过三种方式： 1. Queue 2. Pipe 3. SharedMemory(Value,Array)
无法通过全局变量在进程之间共享信息 (例子中num并不会改变)
```
# 全局变量在多个进程中不能共享
# 在子进程中修改全局变量对父进程中的全局变量没有影响。
# 因为父进程在创建子进程时对全局变量做了一个备份，
# 父进程中的全局变量与子进程的全局变量完全是不同的两个变量。
# 全局变量在多个进程中不能共享

from multiprocessing import Process
from time import sleep

num = 100

def run():
    print("子进程开始")
    global num
    num += 1
    print(f"子进程num：{num}" )
    print("子进程结束")

if __name__ == "__main__":
    print("父进程开始")
    p = Process(target=run)
    p.start()
    p.join()
  # 在子进程中修改全局变量对父进程中的全局变量没有影响
    print("父进程结束。num：%s" % num)
```
#### 队列 (multiprocessing Queue)
进程安全，当一个进程写的时候其他试图写入的进程会被阻塞（锁机制）

q = Queue(maxsize)
q.put(self, obj, block=True, timeout=None) 
q.get(self, block=True, timeout=None) # raise _queue.Empty if nothing can get in time

以下代码就会抛queue.Full, 因为第二个put block设置为false,就是在满的情况下不会阻塞直接抛异常
代码一
``` 
from multiprocessing import Process,Queue
import time

def my_function(queue):
    queue.put(['abc','def'])
    queue.put(['ghi','jkl'], block=False, timeout=None)

if __name__ == '__main__':
    queue = Queue(maxsize=1)
    p = Process(target=my_function,args=(queue,))
    p.start()
    print(queue.get())
    p.join()
```
代码二
``` 
# one process to write and another one to read
from multiprocessing import Process,Queue
import time
def read(queue):
    while True:
        print(queue.get())

def write(queue):
    for word in ['a','b','c','d']:
        time.sleep(1)
        queue.put(word)

if __name__ == '__main__':
    queue = Queue()
    reader = Process(target=read,args=(queue,))
    writer = Process(target=write, args=(queue,))
    reader.start()
    writer.start()
    writer.join()
    reader.terminate()
```
#### 管道
队列底层实现，工作中一般用队列居多
返回的两个连接对象 Pipe() 表示管道的两端。每个连接对象都有 send() 和 recv() 方法（相互之间的）。
请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一端，则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。
``` 
from multiprocessing import Process, Pipe
def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```
#### 共享内存
Value('d', 0.0) # 可以定义类型d是小数, i是整数
Array('i', range(10))
``` 
# 在进行并发编程时，通常最好尽量避免使用共享状态。
# 共享内存 shared memory 可以使用 Value 或 Array 将数据存储在共享内存映射中
# 这里的Array和numpy中的不同，它只能是一维的，不能是多维的。
# 同样和Value 一样，需要定义数据形式，否则会报错
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.14
    for i in a:
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d',0.0)
    arr = Array('i',range(10))
    p = Process(target=f, args=(num,arr))
    p.start()
    p.join()
    print(num.value)
    print(list(arr))

# 将打印
# 3.1415927
# [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
# 创建 num 和 arr 时使用的 'd' 和 'i'
# 参数是 array 模块使用的类型的 typecode ： 'd' 表示双精度浮点数， 'i' 表示有符号整数。
# 这些共享对象将是进程和线程安全的。
```
#### 资源的抢占（加锁机制）
不加锁代码示例， 哪个进程更空闲系统就会调度该进程
``` 
# 进程锁Lock
# 不加进程锁
# 让我们看看没有加进程锁时会产生什么样的结果。
import multiprocessing as mp
import time

def job(v, num):
    for _ in range(5):
        time.sleep(0.1) # 暂停0.1秒，让输出效果更明显
        v.value += num # v.value获取共享变量值
        print(v.value, end="|")

def multicore():
    v = mp.Value('i', 0) # 定义共享变量
    p1 = mp.Process(target=job, args=(v,1))
    p2 = mp.Process(target=job, args=(v,3)) # 设定不同的number看如何抢夺内存
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multicore()

# 在上面的代码中，我们定义了一个共享变量v，两个进程都可以对它进行操作。 
# 在job()中我们想让v每隔0.1秒输出一次累加num的结果，
# 但是在两个进程p1和p2 中设定了不同的累加值。
# 所以接下来让我们来看下这两个进程是否会出现冲突。

# 结论：进程1和进程2在相互抢着使用共享内存v。
```
加锁：
``` 
import multiprocessing as mp
l = mp.lock()
l.acquire() # 获取锁
l.release() #释放锁
```
示例代码
``` 
# 进程锁Lock
# 不加进程锁
# 让我们看看没有加进程锁时会产生什么样的结果。
import multiprocessing as mp
import time
from multiprocessing import Lock
def job(v, num, l):
    l.acquire()
    for _ in range(5):
        time.sleep(0.1) # 暂停0.1秒，让输出效果更明显
        v.value += num # v.value获取共享变量值
        print(v.value, end="|")
    l.release()

def multicore():
    v = mp.Value('i', 0) # 定义共享变量
    l = Lock()
    p1 = mp.Process(target=job, args=(v,1,l))
    p2 = mp.Process(target=job, args=(v,3,l)) # 设定不同的number看如何抢夺内存
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multicore()

# 在上面的代码中，我们定义了一个共享变量v，两个进程都可以对它进行操作。 
# 在job()中我们想让v每隔0.1秒输出一次累加num的结果，
# 但是在两个进程p1和p2 中设定了不同的累加值。
# 所以接下来让我们来看下这两个进程是否会出现冲突。

# 结论：进程1和进程2在相互抢着使用共享内存v。
```
### 进程池
from multiprocessing.pool import Pool
Pool.close() #等待所以子进程结束才结束进程池
Pool.terminate() #暴力结束
可以用with Pool(4) as pool的方式初始化
``` 
from multiprocessing import Process
from multiprocessing.pool import Pool
import multiprocessing as mp
from time import sleep, time
import os,random

def run(name):
    print("%s子进程开始，进程ID：%d" % (name, os.getpid()))
    start = time()
    sleep(random.choice([1, 2, 3, 4]))
    end = time()
    print("%s子进程结束，进程ID：%d。耗时%.4f" % (name, os.getpid(), end-start))


if __name__ == "__main__":
    print("父进程开始")
    # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
    print(f'进程数{mp.cpu_count()}')
    p = Pool(12)
    for i in range(10):
        # 创建进程，放入进程池统一管理
        p.apply_async(run, args=(i,))

    # 如果我们用的是进程池，在调用join()之前必须要先close()，
    # 并且在close()之后不能再继续往进程池添加新的进程
    p.close()
    # 进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程
    p.join()
    print("父进程结束。")
    p.terminate()
```
#### 注意
在p.join()之后试图获取queue的值会造成死锁
``` 
from multiprocessing import Process,Queue
import time

def my_function(queue):
    queue.put(['abc','def'])
    queue.put(['ghi','jkl'], block=True, timeout=None)

if __name__ == '__main__':
    queue = Queue(maxsize=1)
    p = Process(target=my_function,args=(queue,))
    p.start()
    p.join()
    print(queue.get())

```
#### 取到返回结果
result.get can pass in timeout, multiprocessing.context.TimeoutError will be thrown
``` 
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # 进程池包含4个进程
        result = pool.apply_async(f, (10,)) # 执行一个子进程
        print(result.get())        # 显示执行结果

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))        # raises multiprocessing.TimeoutError

```

用进程池实现单进程并发

``` 
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=12) as pool:         # 进程池包含4个进程

        print(pool.map(f, range(10)))       # 输出 "[0, 1, 4,..., 81]"
                    
        it = pool.imap(f, range(10))        # map输出列表，imap输出迭代器
        print(it)
        print(next(it))                     #  "0"
        print(next(it))                     #  "1"
        print(it.next(timeout=1))           #  "4"
```
## 多线程
同一进程下运行，开销小，共享内存
调用方
阻塞  得到调用结果之前，线程会被挂起
非阻塞 不能立即得到结果，不会阻塞线程

被调用方 
同步 得到结果之前，调用不会返回
异步 请求发出后，调用立即返回，没有返回结果，通过回调函数得到实际结果

python 多线程由于GIL的关系只能在一个物理进程里运行
Concurrent = two queues one coffee machine
Parallel = Two Queues two coffee machine

### 创建多线程
面向过程方式
``` 
import threading

def my_func(name):
    print(name)

t1 = threading.Thread(target=my_func, args=('thread1',))
t2 = threading.Thread(target=my_func, args=('thread2',))
t1.start()
t2.start()
```
面向对象方式
``` 
import threading


class MyThreadingClass(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        print(self._name)


t1 = MyThreadingClass('thread 1')
t2 = MyThreadingClass('thread 2')

t1.start()
t2.start()
t1.join()
t2.join()
```
### 线程加锁
普通锁 threading.Lock
可重入锁 
条件锁
信号量

### 线程数据共享
线程之间可以数据共享
#### queue
``` 
import queue
q = queue.Queue(5)
q.put(111)        # 存队列
q.put(222)
q.put(333)
 
print(q.get())    # 取队列
print(q.get())
q.task_done()     # 每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，
                  # 以提示q.join()是否停止阻塞，让线程继续执行或者退出
print(q.qsize())  # 队列中元素的个数， 队列的大小
print(q.empty())  # 队列是否为空
print(q.full())   # 队列是否满了
```

