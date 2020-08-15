##########################################################################
# assignment 1
# 区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
#
# list
# tuple
# str
# dict
# dict
# collections.deque
##########################################################################
# 1. list: 容器，可变
# 2. tuple: 容器，不可变
# 3. str: 扁平，不可变
# 4. dict: 容器，可变
# 5. collections.deque: 容器，可变

##########################################################################
# assignment 2
# 自定义一个 python 函数，实现 map() 函数的功能。
##########################################################################
def myMap(func_arg, iter):
    for i in iter:
        yield func_arg(i)

# testing for assignment 2:
def square(x):
    return x**2

m = myMap(square, range(10))
print(next(m))
print(list(m))

##########################################################################
# assignment 3
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
##########################################################################
import time
def timer(time_out):
    def timer_inner(func):
        def inner(*args):
            start = time.perf_counter()
            func(*args)
            end = time.perf_counter()
            exe_time = end - start

            return f'function finished in {end-start} secs' if exe_time < time_out else 'time out'
        return inner
    return timer

# testing for assignment 3
@timer(1)
def myFunc(a,b,c):
    return a + b + c


print(myFunc(1,2,3))