# Week8 Python Advance

Created: Aug 10, 2020 9:36 PM

# Variable assignment

## mutable type:

- list
- dict

## immutable type:

- int
- float
- string
- tuple

## Container type (can include different types of elements)

- list
- tuple
- collections.deque
- dict

# Sequence

## Type

- container: list, tuple, collections.deque (can have different type element, has copy issue)
- flat: str, bytes, bytearray, memoryview, array.array (can only has one type of element, don't have copy issue)

```python
import copy
copy.copy(object)
copy.deepcopy(object)
```

```python
# 容器序列的拷贝问题
# deep copy or shallow copy only works for container sequence

old_list = [ i for i in range(1, 11)]

new_list1 = old_list
new_list2 = list(old_list) # create a new list

# 切片操作
new_list3 = old_list[:]

# 嵌套对象
old_list.append([11, 12])

import copy
new_list4 = copy.copy(old_list)
new_list5 = copy.deepcopy(old_list)

assert new_list4 == new_list5 #True
assert new_list4 is new_list5 #False AssertionError

old_list[10][0] = 13 # new_list4 will be changed like old_list does but new_list5 will not
```

# dictionary and hash table

- the key in dict has to be immutable

    ```python
    d = {}
    d[123] = 123
    d[[1,2]] = 123
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: unhashable type: 'list'
    ```

- Python collection libs extends the internal data types

    [https://docs.python.org/zh-cn/3.7/library/collections.html](https://docs.python.org/zh-cn/3.7/library/collections.html)

    ```python
    # 命名元组
    from collections import namedtuple
    Point = namedtuple('Ponit', ['x','y'])
    p = Point(10, y=20)
    p.x + p.y
    p[0] + p[1]
    x, y = p
    print(p.x + p.y)
    print(p)

    from collections import Counter
    mystring = ['a','b','c','d','d','d','d','c','c','e']
    # 取得频率最高的前三个值
    cnt = Counter(mystring)
    cnt.most_common(3)
    cnt['b']

    # 双向队列
    from collections import deque
    d = deque('uvw')
    d.append('xyz')
    d.appendleft('rst')
    ```

    计算欧式距离

    __sub __用来重写减号运算符的行为

    ```python
    import numpy as np
    '''
    计算欧式距离
    '''

    vector1 = np.array([1, 2, 3])
    vector2 = np.array([4, 5, 6])

    op1 = np.sqrt(np.sum(np.square(vector1-vector2)))
    op2 = np.linalg.norm(vector1-vector2)

    from collections import namedtuple
    from math import sqrt
    Point = namedtuple('Ponit', ['x','y','z'])

    class Vector(Point):
        def __init__(self, p1, p2, p3):
            super(Vector).__init__()
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3
        
        def __sub__(self, other):
            tmp = (self.p1 - other.p1)**2+(self.p2 - other.p2)**2+(self.p3 - other.p3)**2
            return sqrt(tmp)

    p1 = Vector(1, 2, 3)
    *p2 = Vector(4, 5, 6)*

    p1-p2
    ```

# Function call

- __ call __ make a instance could be used as a function

    ```python
    class Example: 
        def __init__(self): 
            print("Instance Created") 
          
        # Defining __call__ method 
        def __call__(self): 
            print("Instance is called via special method") 
      
    # Instance created 
    e = Example() 
      
    # __call__ method will be called 
    e()

    Example 2:

    class Product: 
        def __init__(self): 
            print("Instance Created") 
      
        # Defining __call__ method 
        def __call__(self, a, b): 
            print(a * b) 
      
    # Instance created 
    ans = Product() 
      
    # __call__ method will be called 
    ans(10, 20)
    ```

# Variable Scope

L(Local) E(enclosing) G(global) B(built in)

```python
# 问题代码1
# def func():
#     var = 100
# func()
# print(var)

# 问题代码2
def func():
    print(var)
func()
var = 100

var = 100
def func():    
    print(var)
func()

# L G
x = 'Global'
def func2():
    x = 'Enclosing'

    def func3():
        x = 'Local'

        print (x)
    func3()
print(x)
func2()

# E
x = 'Global'
def func4():
    x = 'Enclosing'
    def func5():
        return x
    return func5

# assign the reference of func4 to var
var = func4()
print( var() )

# B
print (dir (__builtins__) )
```

# Advanced Function

- function with changeable vars

    ```python
    def func(*args, **kargs):
        print(f'args: {args}')
        print(f'kargs:{kargs}')

    func(123, 'xz', name='xvalue')
    ```

- partial function

    wrap a function with a pre filled args into anohter function ref

    ```python
    from functools import partial

    def multiply(x,y):
            return x * y

    # create a new function that multiplies by 2
    dbl = partial(multiply,2)
    print(dbl(4))
    ```

- Lambda function

    ```python
    # k = lambda x:x+1
    def k(x): 
        return x+1
    ```

- higher order function （高阶函数）

    arg is function, turn function

    ```python
    # map
    def square(x):
        return x**2

    m = map(square, range(10))
    next(m)
    list(m)
    [square(x) for x in range(10)]
    dir(m)

    # reduce
    # reduce(f, [x1, x2, x3]) = f(f(x1, x2), x3)
    from functools import reduce
    def add(x, y):
        return x + y

    reduce(add, [1, 3, 5, 7, 9])
    #25

    # filter
    def is_odd(n):
        return n % 2 == 1

    list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))

    # 偏函数
    def add(x, y):
        return x + y

    import functools
    add_1 = functools.partial(add, 1)
    add_1(10)

    import itertools
    g = itertools.count()
    next(g)
    next(g)
    auto_add_1 = functools.partial(next, g)
    auto_add_1()

    sorted(['bob', 'about', 'Zoo', 'Credit'])
    sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
    sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
    ```

- closure

    ```python
    # version 1
    # 函数是一个对象，所以可以作为某个函数的返回结果
    def line_conf():
        def line(x):
            return 2*x+1
        return line       # return a function object

    my_line = line_conf()
    print(my_line(5))
    ```

    ```python
    # version 2
    # 如果line()的定义中引用了外部的变量
    def line_conf():

        b = 10
        def line(x):
            return 2*x+b
        return line       

    my_line = line_conf()
    print(my_line(5))
    ```

    ```python
    # version 3

    def line_conf():
        b = 10
        def line(x):
            '''如果line()的定义中引用了外部的变量'''
            return 2*x+b
        return line       

    b = -1
    my_line = line_conf()
    print(my_line(5))

    # 编译后函数体保存的局部变量
    print(my_line.__code__.co_varnames)
    # 编译后函数体保存的自由变量
    print(my_line.__code__.co_freevars)
    # 自由变量真正的值
    print(my_line.__closure__[0].cell_contents)  # 10

    #####################
    # 函数和对象比较有哪些不同的属性
    # 函数还有哪些属性
    def func(): 
        pass
    func_magic = dir(func)

    # 常规对象有哪些属性
    class ClassA():
        pass
    obj = ClassA()
    obj_magic = dir(obj)

    # 比较函数和对象的默认属性
    set(func_magic) - set(obj_magic)
    ```

    ```python
    # version 4
    def line_conf(a, b):
        def line(x):
            return a*x + b
        return line

    line1 = line_conf(1, 1)
    line2 = line_conf(4, 5)
    print(line1(5), line2(5))
    ```

    ```python
    # 内部函数对外部函数作用域里变量的引用（非全局变量）则称内部函数为闭包

    def counter(start=0):
       count=[start]
       def incr():
           count[0]+=1
           return count[0]
       return incr

    c1=counter(10)

    print(c1())
    # 结果：11
    print(c1())
    # 结果：12

    # nonlocal访问外部函数的局部变量
    # 注意start的位置，return的作用域和函数内的作用域不同
    def counter2(start=0):
        def incr():
            nonlocal start  # make the local variable to be the enclosing variable
            start+=1
            return start
        return incr
    c1=counter2(5)
    print(c1())
    print(c1())

    c2=counter2(50)
    print(c2())
    print(c2())

    print(c1())
    print(c1())

    print(c2())
    print(c2())
    ```

    nonlocal example:

    ```python
    def myfunc1():
      x = "John"
      def myfunc2():
        x = "hello"
      myfunc2()
      return x

    print(myfunc1())  # John

    def myfunc1():
      x = "John"
      def myfunc2():
    		nonlocal x
        x = "hello"
      myfunc2()
      return x

    print(myfunc1())  # hello
    ```

# Decorator

Decorator need to pass in a reference to the decorated function

enhance but not change the original function

check PEP 318 and PEP-3129 if have time

```python
# PEP 318 装饰器  PEP-3129 类装饰器

# 前置问题
def func1():
    pass
a=func1
b=func1()

# func1 表示函数
# func1() 表示执行函数

############################
# 装饰器, @ 语法糖
@decorate   
def func2():
    print('do sth')

# 等效于下面
def func2():
    print('do sth')
func2 = decorate(func2)

#############################
# 装饰器在模块导入的时候自动运行
# testmodule.py
def decorate(func):
    print('running in modlue')
    def inner():
        return func()
    return inner

@decorate
def func2():
    pass

# test.py
import testmodule
# from testmodule import func2
```

Decorator used in flask

```python
# 用在哪里
# Flask 的装饰器是怎么用的？
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
   return '<h1>hello world </h1>'

# app.add_url_rule('/', 'index')

if __name__ == '__main__':
   app.run(debug=True)

# 注册
@route('index',methods=['GET','POST'])
def static_html():
    return  render_template('index.html')
```

- decorator with multiple layers

    ```python
    # 包装
    def html(func):
        def decorator():
            return f'<html>{func()}</html>'
        return decorator

    def body(func):
        def decorator():
            return f'<body>{func()}</body>'
        return decorator

    @html
    @body
    def content():
        return 'hello world'

    content()
    ```

- Decorated method has arguments

    note that foo.__name __ will print out inner. If we want to keep the  orignal func name we need to annotate with @wraps(func) up on the inner method. wraps imported from functools

    ```python
    # 被修饰函数带参数
    def outer(func):
        def inner(a,b):
            print(f'inner: {func.__name__}')
            print(a,b)
            func(a,b)
        return inner

    @outer
    def foo(a,b):
        print(a+b)
        print(f'foo: {foo.__name__}')
        
        
    foo(1,2)
    foo.__name__

    # 被修饰函数带不定长参数

    def outer2(func):
        def inner2(*args,**kwargs):
            func(*args,**kwargs)
        return inner2

    @outer2
    def foo2(a,b,c):
        print(a+b+c)
        
    foo2(1,3,5)

    # 被修饰函数带返回值

    def outer3(func):
        def inner3(*args,**kwargs):
            ###
            ret = func(*args,**kwargs)
            ###
            return ret
        return inner3

    @outer3
    def foo3(a,b,c):
        return (a+b+c)
        
    print(foo3(1,3,5))
    ```

    - Decorator has parameters

    Add another layer to wrap the outer method

    ```python
    # 装饰器带参数 

    def outer_arg(bar):
        def outer(func):
            def inner(*args,**kwargs):
                ret = func(*args,**kwargs)
                print(bar)
                return ret
            return inner
        return outer

    # 相当于outer_arg('foo_arg')(foo)()
    @outer_arg('foo_arg')
    def foo(a,b,c):
        return (a+b+c)
        
    print(foo(1,3,5))
    ```

    - Built in decorator

    ```python
    ########################
    # 内置的装饰方法函数

    # functools.wraps
    # @wraps接受一个函数来进行装饰
    # 并加入了复制函数名称、注释文档、参数列表等等的功能
    # 在装饰器里面可以访问在装饰之前的函数的属性
    # @functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
    # 用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器。 
    # 它等价于 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)。

    from time import ctime,sleep
    from functools import wraps
    def outer_arg(bar):
        def outer(func):
            # 结构不变增加wraps
            @wraps(func)
            def inner(*args,**kwargs):
                print("%s called at %s"%(func.__name__,ctime()))
                ret = func(*args,**kwargs)
                print(bar)
                return ret
            return inner
        return outer

    @outer_arg('foo_arg')
    def foo(a,b,c):
        """  __doc__  """
        return (a+b+c)
        
    print(foo.__name__)

    ########################
    # flask 使用@wraps()的案例
    from functools import wraps
     
    def requires_auth(func):
        @wraps(func)
        def auth_method(*args, **kwargs):
            if not auth:
                authenticate()
            return func(*args, **kwargs)
        return auth_method

    @requires_auth
    def func_demo():
        pass

    ########################

    from functools import wraps
     
    def logit(logfile='out.log'):
        def logging_decorator(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                log_string = func.__name__ + " was called"
                print(log_string)
                with open(logfile, 'a') as opened_file:
                    opened_file.write(log_string + '\n')
                return func(*args, **kwargs)
            return wrapped_function
        return logging_decorator
     
    @logit()
    def myfunc1():
        pass
     
    myfunc1()
    # Output: myfunc1 was called
     
    @logit(logfile='func2.log')
    def myfunc2():
        pass
     
    myfunc2()

    # Output: myfunc2 was called
    ```

    LRUCach,  cache the result of a method 

    LRU is a mechanism which will delete the old cache based conditionally

    For the example below if use LRU cache will just run like 0.13 sec but if not will run above 4 secs

    ```python
    # functools.lru_cache
    # 《fluent python》的例子
    # functools.lru_cache(maxsize=128, typed=False)有两个可选参数
    # maxsize代表缓存的内存占用值，超过这个值之后，就的结果就会被释放
    # typed若为True，则会把不同的参数类型得到的结果分开保存
    import functools
    @functools.lru_cache()
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-2) + fibonacci(n-1)

    if __name__=='__main__':
        import timeit
        print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))
    ```

    - Use class to be decorator

    Have to implement __call __ method. __ call __ is used for make an instance to be callable like a function.

    ```python
    # Python 2.6 开始添加类装饰器
    from functools import wraps

    class MyClass(object):
        def __init__(self, var='init_var', *args, **kwargs):
            self._v = var
            super(MyClass, self).__init__(*args, **kwargs)
        
        def __call__(self, func):
            # 类的函数装饰器
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                func_name = func.__name__ + " was called"
                print(func_name)
                return func(*args, **kwargs)
            return wrapped_function

    @MyClass(100)
    def myfunc():
        pass

    myfunc()

    # 另一个示例
    class Count(object):
        def __init__(self,func):
            self._func = func
            self.num_calls = 0
        
        def __call__(self, *args, **kargs):
            self.num_calls += 1
            print(f'num of call is {self.num_calls}')
            return self._func()

    @Count
    def example():
        print('hello')

    example()
    print(type(example))
    ```

    - Use decorator to decorate class

    the method define in the decorator will override the method in decorated class

    ```python
    # 装饰类
    def decorator(aClass):
        class newClass(object):
            def __init__(self, args):
                self.times = 0
                self.wrapped = aClass(args)
                
            def display(self):
                # 将runtimes()替换为display()
                self.times += 1
                print("run times", self.times)
                self.wrapped.display()
        return newClass

    @decorator
    class MyClass(object):
        def __init__(self, number):
            self.number = number
        # 重写display
        def display(self):
            print("number is",self.number)

    six = MyClass(6)
    for i in range(5):
        six.display()
    ```

    ```python
    # 官方文档装饰器的其他用途举例

    # 向一个函数添加属性
    def attrs(**kwds):
        def decorate(f):
            for k in kwds:
                setattr(f, k, kwds[k])
            return f
        return decorate

    @attrs(versionadded="2.2",
           author="Guido van Rossum")
    def mymethod(f):
        pass

    ##############################

    # 函数参数观察器
    import functools
    def trace(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            print(f, args, kwargs)
            result = f(*args, **kwargs)
            print(result)
        return decorated_function
    @trace
    def greet(greeting, name):
        return '{}, {}!'.format(greeting, name)

    greet('better','me')

    ############################################

    # Python3.7 引入 Data Class  PEP557

    class MyClass:
        def __init__(self, var_a, var_b):
            self.var_a = var_a
            self.var_b = var_b

        def __eq__(self, other):
            if self.__class__ is not other.__class__:
                return False
            return (self.var_a, self.var_b) == (other.var_a, other.var_b)
            
    var3 = MyClass('x','y')
    var4 = MyClass('x','y')

    var3 == var4

    from dataclasses import dataclass
    @dataclass
    class MyClass:
        var_a: str  # this is a type hint
        var_b: str

    var_1 = MyClass('x','y')
    var_2 = MyClass('x','y')

    # 不用在类中重新封装 __eq__

    var_1 == var_2
    # 存在的问题: var_a var_b不能作为类属性访问

    ##########################

    # 如下的类装饰器实现了一个用于类实例属性的Private声明
    # 属性存储在一个实例上，或者从其一个类继承而来
    # 不接受从装饰的类的外部对这样的属性的获取和修改访问
    # 但是，仍然允许类自身在其方法中自由地访问那些名称
    # 类似于Java中的private属性

    traceMe = False
    def trace(*args):
        if traceMe:
            print('['+ ' '.join(map(str,args))+ ']')

    def Private(*privates):
        def onDecorator(aClass):
            class onInstance:
                def __init__(self,*args,**kargs):
                    self.wrapped = aClass(*args,**kargs)
                def __getattr__(self,attr):
                    trace('get:',attr)
                    if attr in privates:
                        raise TypeError('private attribute fetch:'+attr)
                    else:
                        return getattr(self.wrapped,attr)
                def __setattr__(self,attr,value):
                    trace('set:',attr,value)
                    if attr == 'wrapped': # 这里捕捉对wrapped的赋值
                        self.__dict__[attr] = value
                    elif attr in privates:
                        raise TypeError('private attribute change:'+attr)
                    else: # 这里捕捉对wrapped.attr的赋值
                        setattr(self.wrapped,attr,value)
            return onInstance
        return onDecorator

    if __name__ == '__main__':
        traceMe = True

        @Private('data','size')
        class Doubler:
            def __init__(self,label,start):
                self.label = label
                self.data = start
            def size(self):
                return len(self.data)
            def double(self):
                for i in range(self.size()):
                    self.data[i] = self.data[i] * 2
            def display(self):
                print('%s => %s'%(self.label,self.data))

        X = Doubler('X is',[1,2,3])
        Y = Doubler('Y is',[-10,-20,-30])
        print(X.label)
        X.display()
        X.double()
        X.display()
        print(Y.label)
        Y.display()
        Y.double()
        Y.label = 'Spam'
        Y.display()

        # 这些访问都会引发异常
        print(X.size())
        print(X.data)
        X.data = [1,1,1]
        X.size = lambda S:0
        print(Y.data)
        print(Y.size())

    # 这个示例运用了装饰器参数等语法，稍微有些复杂，运行结果如下：
    # [set: wrapped <__main__.Doubler object at 0x03421F10>]
    # [set: wrapped <__main__.Doubler object at 0x031B7470>]
    # [get: label]
    # X is
    # [get: display]
    # X is => [1, 2, 3]
    # [get: double]
    # [get: display]
    # X is => [2, 4, 6]
    # [get: label]
    # Y is
    # [get: display]
    # Y is => [-10, -20, -30]
    # [get: double]
    # [set: label Spam]
    # [get: display]
    ```

# Duck typing(__ getitem__, __ setitem__...)

- duck typing —- make the customized class to mimic the built in types

    ```python
    class Foo(object):
        # 用与方法返回
        def __str__(self):
            return '__str__ is called'

        # 用于字典操作
        def __getitem__(self, key):
            print(f'__getitem__ {key}') 
        
        def __setitem__(self, key, value):
            print(f'__setitem__ {key}, {value}')
        
        def __delitem__(self, key):
            print(f'__delitem__ {key}')

        # 用于迭代
        def __iter__(self):
            return iter([i for i in range(5)])

    # __str__
    bar = Foo()
    print(bar)

    # __XXitem__
    bar['key1']
    bar['key1']='value1'
    del bar['key1']

    # __iter__
    for i in bar:
        print(i)
    ```

- Format string

    __ str__ and __ repr__ is quite similar just repr is more used for print the real object ( when communicate betwen two object it use __ repr__ ) while str is for human read

    ```python
    import math
    # different ways for formating string
    print('The value of Pi is approximately %5.3f.' % math.pi)

    print('{1} and {0}'.format('spam', 'eggs'))

    print('The story of {0}, {1}, and {other}.'.format(
        'Bill', 'Manfred', other='Georg'))

    firstname = 'yin'
    lastname = 'wilson'
    print('Hello, %s %s.' % (lastname, firstname))
    print('Hello, {1} {0}.'.format(firstname, lastname))
    print(f'Hello, {lastname} {firstname}.')

    f'{ 2 * 5 }'

    class Person:
        def __init__(self, first_name, last_name):
            self.first_name = first_name
            self.last_name = last_name

        def __str__(self):
            return f'hello, {self.first_name} {self.last_name}.'

        def __repr__(self):
            return f'hello, {self.first_name} {self.last_name}.'

    me = Person('yin', 'wilson')

    print(f'{me}')
    ```

- Type hint

    ```python
    # typing 类型注解(type hint)

    # Hint only

    def func(text: str, number: int) -> str:
        return text * number

    func('a', 5)
    ```