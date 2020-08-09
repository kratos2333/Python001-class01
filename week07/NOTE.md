# Week 7 Object Oriented

# Class and Object

## Magic method

- __ dict __: normally be used to show the attribuftes belong to an instance

## Fields

- Class fields — one copy in memory
- Object fields — each instance will have a copy

```python
# GOD
class Human(object):
    # 静态字段
    live = True

    def __init__(self, name):
        # 普通字段
        self.name = name

man = Human('Adam')
woman = Human('Eve')

# 有静态字段,live属性
print(Human.__dict__)
# 有普通字段,name属性
print(man.__dict__)

# 实例可以使用普通字段也可以使用静态字段
man.name
man.live = False
# 查看实例属性
print(man.__dict__) #普通字段有live变量
print(man.live)
print(woman.live)

# 类可以使用静态字段
print(Human.live)

# 可以为类添加静态字段
Human.newattr = 1
print(dir(Human))
print(Human.__dict__)
```

- Add new field for target class/object

    ```python
    setattr(MyClass, 'newattr', 'value')

    # cannot add attr on to the built in class
    # followings is wrong
    setattr(list, 'newattr', 'value')
    ```

- field type

    ```python
    class Human2(object):
        # 人为约定不可修改
        _age = 0

        # 私有属性
        __fly = False

        # 魔术方法，不会自动改名
        # 如 __init__

    # 自动改名机制 _Human2__fly
    print(Human2.__dict__)

    #output
    {'__module__': '__main__', '_age': 0, '_Human2__fly': False, 
    '__dict__': <attribute '__dict__' of 'Human2' objects>, 
    '__weakref__': <attribute '__weakref__' of 'Human2' objects>, '__doc__': None}
    ```

    Still can change the private field if change Human2._Human2__fly 

- get all the subclasses under object

    ```python
    ().__class__.__base__[0].__subclasses__()

    # tuple class, we also can use [] doesn't matter
    ().__class__ 

    # get the parent class in tuple
    ().__class__.__bases__

    # take the first which will return object
    ().__class__.__bases__[0]

    # return all the sub classes
    ().__class__.__base__[0].__subclasses__()
    ```

## Class Method

- @classMethod

    the cls could be used in child class overloading cls will become the child class when invoke from child

    ```python
    # 让实例的方法成为类的方法
    class Kls1(object):
        bar = 1
        def foo(self):
            print('in foo')
        # 使用类属性、方法
        @classmethod
        def class_foo(cls):  # cls will beome Kls1
            print(cls.bar)
            print(cls.__name__)
            cls().foo()

    Kls1.class_foo()

    # instance or object can both call classmethod
    class Story(object):
        snake = 'Python'
        def __init__(self, name):
            self.name = name
        # 类的方法
        @classmethod
        def get_apple_to_eve(cls):
            return cls.snake

    s = Story('anyone')
    # get_apple_to_eve 是bound方法，查找顺序是先找s的__dict__是否有get_apple_to_eve,如果没有，查类Story
    print(s.get_apple_to_eve)
    # 类和实例都可以使用
    print(s.get_apple_to_eve())
    print(Story.get_apple_to_eve())
    ```

- classMethod usage (mimicing java multiple constructors)

    ```python
    ## example 1:
    class Kls3():
        def __init__(self, fname, lname):
            self.fname = fname
            self.lname = lname

        @classmethod
        def pre_name(cls,name):
            fname, lname = name.split('-')
            return cls(fname, lname)

        def print_name(self):
            print(f'first name is {self.fname}')
            print(f'last name is {self.lname}')

    me3 = Kls3.pre_name('wilson-yin')
    me3.print_name()

    # example 2:
    # '''
    # 类方法用在模拟java定义多个构造函数的情况。
    # 由于python类中只能有一个初始化方法，不能按照不同的情况初始化类。
    # '''
    class Book(object):

        def __init__(self, title):
            self.title = title

        @classmethod
        def create(cls):
            book = cls(title='Default title')
            return book

    book1 = Book("python")
    book2 = Book.create()
    print(book1.title)
    print(book2.title)
    ```

- classMethod usage2 (define the classmethod in parent and child class can has overloading)

    Each child class will have a copy of the class field. Check the total in the example below

    ```python
    class Fruit(object):
        total = 0

        @classmethod
        def print_total(cls):
            print(cls.total)
            print(id(Fruit.total))
            print(id(cls.total))

        @classmethod
        def set(cls, value):
            print(f'calling {cls} ,{value}')
            cls.total = value

    class Apple(Fruit):
        pass

    class Orange(Fruit):
        pass

    Apple.set(100)
    # calling <class '__main__.Apple'> ,100
    Orange.set(200)

    # calling <class '__main__.Orange'> ,200
    org=Orange()
    org.set(300)

    # calling <class '__main__.Orange'> ,300
    Apple.print_total()
    # 100
    # 140735711069824
    # 140735711073024
    Orange.print_total()
    # 300
    # 140735711069824
    # 1998089714064
    ```

## Static method

```python
import datetime
class Story(object):
    snake = 'Python'
    def __init__(self, name):
        self.name = name
    # 静态的方法
    @staticmethod
    def god_come_go():
        if datetime.datetime.now().month % 2 :
             print('god is coming')
    
Story.god_come_go()

# 静态方法可以由类直接调用
# 因为不传入self 也不传入 cls ，所以不能使用类属性和实例属性
```

## Access attribute

when call a field not exists, **getattribute** will be invoked and raise AttributeError

- __ **getattribute __**() . All attributes evoking will call this method

```python
class Human(object):  
    # 接收参数  
    def __init__(self, name):
        self.name = name

h1 = Human('Adam')
h2 = Human('Eve')

# 对实例属性做修改
h1.name = 'python'

# 对实例属性查询
print(h1.name)

# 删除实例属性
del h1.name

# AttributeError，访问不存在的属性
# 由__getattribute__(self,name)抛出
print(h1.name)
```

we can override __ getatttribute __(self,name)

```python
class Human2(object):
    """
    getattribute对任意读取的属性进行截获
    """
    def __init__(self):
        self.age = 18
    def __getattribute__(self,item):
        print(f' __getattribute__ called item:{item}')

h1 = Human2()

h1.age
h1.noattr
```

usage1  we can use it like a intercepter

```python
class Human2(object):  
    """
    拦截已存在的属性
    """  
    def __init__(self):
        self.age = 18
    def __getattribute__(self,item):
        print(f' __getattribute__ called item:{item}')
        return super().__getattribute__(item)
h1 = Human2()

print(h1.age)
# 存在的属性返回取值
print(h1.noattr)
# 不存在的属性返回 AttributeError
```

usage 2 add an not existing attribute

```python
# instead throwing exception we set a default value for it
class Human2(object):    
    def __getattribute__(self, item):
        """
        将不存在的属性设置为100并返回,模拟getattr行为
        """
        print('Human2:__getattribute__')
        try:
            return super().__getattribute__(item)
        except Exception as e:
            self.__dict__[item] = 100
            return 100
h1 = Human2()

print(h1.noattr)
```

- __ **getattr** __(). Only the undefined attrs will call this method

```python
class Human2(object):  
    def __init__(self):
        self.age = 18

    def __getattr__(self, item): 
        # 对指定属性做处理:fly属性返回'superman',其他属性返回None
        self.item = item
        if self.item == 'fly':
            return 'superman'

h1 = Human2()

print(h1.age)
print(h1.fly)
print(h1.noattr)
```

如果同时存在，执行顺序是 __getattribute__ > __getattr__ > **dict**

```python
class Human2(object):    
    """
    同时存在的调用顺序
    """
    def __init__(self):
        self.age = 18

    def __getattr__(self, item): 

        print('Human2:__getattr__')
        return 'Err 404 ,你请求的参数不存在'

    def __getattribute__(self, item):
        print('Human2:__getattribute__')
        return super().__getattribute__(item)

h1 = Human2()

# 如果同时存在，执行顺序是 __getattribute__ > __getattr__ > __dict__
print(h1.age)
print(h1.noattr)
# 注意输出，noattr的调用顺序
```

# Descriptor

- __ get __, __ set __ , __ del __  (underline method, just need to know about that )

    ```python
    # __getattribute__ 的底层原理是描述器
    class Desc(object):
        """
        通过打印来展示描述器的访问流程
        """
        def __init__(self, name):
            self.name = name
        
        def __get__(self, instance, owner):
            print(f'__get__{instance} {owner}')
            return self.name

        def __set__(self, instance, value):
            print(f'__set__{instance} {value}')
            self.name = value

        def __delete__(self, instance):
            print(f'__delete__{instance}')
            del self.name

    class MyObj(object):
        a = Desc('aaa')
        b = Desc('bbb')

    my_object = MyObj()
    print(my_object.a)

    my_object.a = 456
    print(my_object.a)
    ```

- @property  (quite similar to java's getter and setter)

    ```python
    class Human(object):
        def __init__(self, name):
            self.name = name

        # 将方法封装成属性
        @property
        def gender(self):
            return 'M'

    h1 = Human('Adam')
    h2 = Human('Eve')
    print(h1.gender) # print M

    # AttributeError:
    h2.gender = 'F'
    ```

    example with setter and del

    ```python
    class Human2(object):
        def __init__(self):
            self._gender = None
        # 将方法封装成属性
        @property
        def gender2(self):
            print(self._gender)

        # 支持修改
        @gender2.setter
        def gender2(self,value):
            self._gender = value

        # 支持删除
        @gender2.deleter
        def gender2(self):
            del self._gender

    h = Human2()
    h.gender2 = 'F'
    print(h.gender2)
    h.gender2 = 'M'
    print(h.gender2)
    del h.gender2

    # 被装饰函数建议使用相同的gender2
    # 使用setter 并不能真正意义上实现无法写入，gender被改名为 _Article__gender

    # property本质并不是函数，而是特殊类（实现了数据描述符的类）
    # 如果一个对象同时定义了__get__()和__set__()方法，则称为数据描述符，
    # 如果仅定义了__get__()方法，则称为非数据描述符

    # property的优点：
    # 1 代码更简洁，可读性、可维护性更强。
    # 2 更好的管理属性的访问。
    # 3 控制属性访问权限，提高数据安全性。

    # use __ get __ and __ set__ to impl property
    # 限制传入的类型和范围（整数，且满足18-65）
    class Age(object):
        def __init__(self, default_age = 18):
            self.age_range = range(18,66)
            self.default_age = default_age
            self.data = {}

        def __get__(self, instance, owner):
            return self.data.get(instance, self.default_age)
        
        def __set__(self, isinstance, value):
            if value not in self.age_range:
                raise ValueError('must be in (18-65)')

            self.data[isinstance] = value

    class Student(object):
        age = Age()

    if __name__ == '__main__':
        s1 = Student()
        s1.age = 30
        s1.age = 100
    ```

    use property to handle password

    ```python
    # 使用装饰器完成password的读取和写入功能分离
        @property
        def password(self):
            return None
        
        @password.setter
        def password(self, password):
            self.password_hash = generate_password_hash(password)
        
        def verify_password(self, password):
            return check_password_hash(self.password_hash, password)
        
      
        def is_active(self):
            return True
    ```

# Object oriented (everything is object)

relationship between object and type(元类）:

- object 和 type 都属于 type 类 (class 'type')
- type 类由 type 元类自身创建的。object 类是由元类 type 创建
- object 的父类为空，没有继承任何类
- type 的父类为 object 类 (class 'object') — this can be prove by print(type.__ **class__**.__ **bases__**[0])

    type create object but doesn't mean type is the parent class of object

    ```python
    # 父类
    class People(object):
        def __init__(self, name):
            self.gene = 'XY'
            # 假设人人都有名字
            self.name = name
        def walk(self):
            print('I can walk')

    # 子类
    class Man(People):
        def __init__(self,name):
            # 找到Man的父类People，把类People的对象转换为类Man的对象
            super().__init__(name)

        def work(self):
            print('work hard')

    class Woman(People):
        def __init__(self,name):
            super().__init__(name)
        def shopping(self):
            print('buy buy buy')

    p1 = Man('Adam')
    p2 = Woman('Eve')

    # 问题1 gene有没有被继承？
    # super(Man,self).__init__()
    p1.gene

    # 问题2 People的父类是谁？
    # object 与 type
    print('object', object.__class__, object.__bases__)
    print('type', type.__class__, type.__bases__)
    # type元类由type自身创建，object类由元类type创建
    # type类继承了object类

    # 问题3 能否实现多重层级继承

    # 问题4 能否实现多个父类同时继承 
    class Son(Man, Woman):
        pass

    # 新的问题： 继承顺序
    # 钻石继承
    ```

    ## Diamond inheritance

    diamond inheritance (MRO stand for method resolution order)

    ```python
    # 钻石继承
    class BaseClass(object):
        num_base_calls = 0
        def call_me(self):
            print ("Calling method on Base Class")
            self.num_base_calls += 1

    class LeftSubclass(BaseClass):
        num_left_calls = 0
        def call_me(self):
            print ("Calling method on Left Subclass")
            self.num_left_calls += 1

    class RightSubclass(BaseClass):
        num_right_calls = 0
        def call_me(self):
            print("Calling method on Right Subclass")
            self.num_right_calls += 1

    class Subclass(LeftSubclass,RightSubclass):
        pass

    a = Subclass()
    a.call_me()

    print(Subclass.mro())
    # 广度优先， 另外Python3 中不加(object)也是新式类，但是为了代码不会误运行在python2下产生意外结果，仍然建议增加
    # >>> Subclass.mro()
    # [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.RightSubclass'>, <class '__main__.BaseClass'>, <class 'object'>]

    #  修改RightSubclass 的 父类为 Object
    # >>> Subclass.mro()
    # [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.BaseClass'>, <class '__main__.RightSubclass'>, <class 'object'>]
    ```

## DAG （directed Acyclic graph)） 有向无环路图来分析继承

DAG 原本是一种数据结构，因为 DAG 的拓扑结构带来的优异特性，经常被用于处
理动态规划、寻求最短路径的场景

![Week%207%20Object%20Oriented%207eb0ea122fe94672a8e9e4094d2bb80d/Untitled.png](Week%207%20Object%20Oriented%207eb0ea122fe94672a8e9e4094d2bb80d/Untitled.png)

```python
# 钻石继承
class BaseClass(object):
    num_base_calls = 0
    def call_me(self):
        print ("Calling method on Base Class")
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    num_left_calls = 0
    def call_me(self):
        print ("Calling method on Left Subclass")
        self.num_left_calls += 1

class RightSubclass(object):
    num_right_calls = 0
    def call_me(self):
        print("Calling method on Right Subclass")
        self.num_right_calls += 1

class Subclass(LeftSubclass,RightSubclass):
    pass

a = Subclass()
a.call_me()

print(Subclass.mro())
#  修改RightSubclass 的 父类为 Object
# >>> Subclass.mro()
# [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.BaseClass'>, <class '__main__.RightSubclass'>, <class 'object'>]
```

# Design Pattern

# SOLID

- The single responsibility principle
- The open closed principle
- The liskov substitution principle
- The interface segregation principle
- The dependency inversion principle

## Singleton

- diff between __new __ and __ init __

    new 才是构造方法， init是初始化方法

    - new__ 是实例创建之前被调用，返回该实例对象，是静态方法
    - init__ 是实例对象创建完成后被调用，是实例方法
    - new__ 先被调用，**init** 后被调用
    - new__ 的返回值（实例）将传递给 __init__ 方法的第一个参数，__init__ 给这个
    实例设置相关参数
    - How to impl singleton (use decorator or __ new__)

        ```python
        # 装饰器实现单实例模式
        def singleton(cls):
            instances = {}
            def getinstance():
                if cls not in instances:
                    instances[cls] = cls()
                return instances[cls]
            return getinstance

        @singleton
        class MyClass:
            pass

        m1 = MyClass()
        m2 = MyClass()
        print(id(m1))
        print(id(m2))
        ```

        ```python
        # __new__ 与 __init__ 的关系
        class Foo(object):
            def __new__(cls, name):
                print('trace __new__')
                return super().__new__(cls)
            
            def __init__(self, name):
                print('trace __init__')
                super().__init__()
                self.name = name

        bar = Foo('test')
        bar.name

        #相当于在执行下面的操作
        bar = Foo.__new__(Foo, 'test')
        if isinstance(bar, Foo):
            Foo.__init__(bar, 'test')
        ```

        use __ new __ to impl singleton

        ```python

        ```

    ## Factory pattern

    ### Simple factory pattern

    ```python
    class Human(object):
        def __init__(self):
            self.name = None
            self.gender = None

        def getName(self):
            return self.name

        def getGender(self):
            return self.gender

    class Man(Human):
        def __init__(self, name):
            print(f'Hi,man {name}')

    class Woman(Human):
        def __init__(self, name):
            print(f'Hi,woman {name}')

    class Factory:
        def getPerson(self, name, gender):
            if gender == 'M':
                return Man(name)
            elif gender == 'F':
                return Woman(name)
            else:
                pass

    if __name__ == '__main__':
        factory = Factory()
        person = factory.getPerson("Adam", "M")
    ```

    Dynamically create class (在框架里会经常看到）

    ```python
    # 返回在函数内动态创建的类
    def factory2(func):
        class klass: pass
        #setattr需要三个参数:对象、key、value
        setattr(klass, func.__name__, func)
        print(klass.__dict__)
        return klass

    def say_foo(self): 
        print('bar')

    Foo = factory2(say_foo)
    foo = Foo() #实例化
    foo.say_foo()

    # or we can set func to be the classmethod
    def factory2(func):
        class klass: pass
        #setattr需要三个参数:对象、key、value
        # setattr(klass, func.__name__, func)
        setattr(klass, func.__name__, classmethod(func))
        return klass

    def say_foo(self): 
        print('bar')

    Foo = factory2(say_foo)
    Foo.say_foo()
    ```

# Metaclass (经常用于框架，不大会用，但是要能读懂）

- 在类刚开始创建的时候进行拦截，增加相应功能
- 元类是创建类的类，是类的模板
- 元类是用来控制如何创建类的，正如类是创建对象的模板一样。
- 创建元类的两种方法
    - class
    - type (参数：类名，父类的元祖，类的成员)

```python
# 使用type元类创建类
def hi():
    print('Hi metaclass')

# type的三个参数:类名、父类的元组、类的成员
# say_hi point to the ref funtion hi
Foo = type('Foo',(),{'say_hi':hi})
foo = Foo
foo.say_hi()
# 元类type首先是一个类，所以比类工厂的方法更灵活多变，可以自由创建子类来扩展元类的能力
```

```python
def pop_value(self, dict_value):
    for key in self.keys():
        if self.__getitem__(key) == dict_value:
        # same as
        # if self[key] == dict_value:
            self.pop(key)
            break

# 元类要求,必须继承自type
class DelValue(type):
    # 元类要求，必须实现new方法
    # name, parent, attrs
    def __new__(cls, name, bases, attrs):
        attrs['pop_value'] = pop_value
        return type.__new__(cls, name, bases, attrs)

# when create this class pass in a metaclass to change the behavior
class DelDictValue(dict, metaclass=DelValue):
    # in python2 need to add the following
    # __metaclass__ = DelValue
    pass

d = DelDictValue()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

# note that this d object has a method allowing pass in a value then pop that key value pair
# this is not a standard pop function in diction
d.pop_value('C')
for k, v in d.items():
    print(k, v)
```

# Abstract Class

- 抽象基类（abstract base class，ABC）用来确保派生类实现了基类中的特定方法
- 使用抽象基类的好处：
    - 避免继承错误，使类层次易于理解和维护。
    - 无法实例化基类。
    - 如果忘记在其中一个子类中实现接口方法，要尽早报错

child class has to impl the method annotated with @abstractmethod

```python
from abc import ABCMeta, abstractmethod
class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass
    @abstractmethod
    def bar(self):
        pass

class Concrete(Base):
    def foo(self):
        pass

c = Concrete() # TypeError
```

# Mixin

在程序运行过程中，重定义类的继承，即动态继承。好处：
• 可以在不修改任何源代码的情况下，对已有类进行扩展
• 进行组件的划分

```python
def mixin(Klass, MixinKlass):
    Klass.__bases__ = (MixinKlass,) + Klass.__bases__

class Fclass(object):
    def text(self):
        print('in FatherClass')

class S1class(Fclass):
    pass

class MixinClass(object):
    def text(self):
        return super().text()
        # print('in MixinClass')

class S2class(S1class, MixinClass):
    pass

print(f' test1 : S1class MRO : {S1class.mro()}')
s1 = S1class()
s1.text()

mixin(S1class, MixinClass)
print(f' test2 : S1class MRO : {S1class.mro()}')
s1 = S1class()
s1.text()

print(f' test3 : S2class MRO : {S2class.mro()}')
s2 = S2class()
s2.text()
```

More complicated example

```python
# 《Python GUI Programming with Tkinter》
# Mixin类无法单独使用，必须和其他类混合使用，来加强其他类

class Displayer():
    def display(self, message):
        print(message)

class LoggerMixin():
    def log(self, message, filename='logfile.txt'):
        with open(filename, 'a') as fh:
            fh.write(message)

    def display(self, message):
        # 其实这里的super可以理解为下一个mro执行处
        super(LoggerMixin, self).display(message)
        self.log(message)

class MySubClass(LoggerMixin, Displayer):
    def log(self, message):
        super().log(message, filename='subclasslog.txt')

subclass = MySubClass()
subclass.display("This string will be shown and logged in subclasslog.txt")
print(MySubClass.mro())
```