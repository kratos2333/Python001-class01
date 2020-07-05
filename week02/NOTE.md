# 第二周 学习笔记
## 异常的捕获与处理
常见的异常类型主要有：
1. IndexError,KeyError
2. IOError
3. NameError
4. TypeError
5. AttributeError
6. ZeroDivisionError

###捕获多个异常
``` 
try:
    f3()
except (ZeroDivisionError,Exception) as e:
    print(e)  
```

###自定义异常
``` 
class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

userinput = 'a'

try:
    if (not userinput.isdigit()):
        raise UserInputError('用户输入错误')
except UserInputError as ue:
    print(ue)
finally:
    del userinput
```

###美化异常输出pretty_errors
``` 
import pretty_errors
1/0
print('never see me')
```
###自定义带上下文的类
``` 
class Open:
    def __enter__(self):
        print("open")

    def __exit__(self, type, value, trace):
        print("close")
 
    def __call__(self):
        pass

with Open() as f:
    pass
# 上下文协议
```
###魔术方法__call__
``` 
class Point:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __call__(self, y,z):
        self.y = y
        self.z = z

    def __str__(self):
        return f'x: {self.x}  y: {self.y}  z: {self.z}'

p1 = Point(1,2,3)
print(p1)  # x: 1  y: 2  z: 3
p1(3,4)
print(p1) # x: 1  y: 3  z: 4

```
## PyMySql进行数据库操作
###安装
``` 
pip install pymysql
```
###基本操作
``` 
conn = pymysql.connect(host = 'localhost',
                       port = 3306,
                       user = 'root',
                       password = 'rootroot',
                       database = 'test',
                       charset = 'utf8mb4'
                        )

# 获得cursor游标对象
con1 = conn.cursor()

# 操作的行数
count = con1.execute('select * from tb1;')

# 获得一条查询结果
result = con1.fetchone()
print(result)

# 获得所有查询结果
print(con1.fetchall())

# 单条数据插入
# con1.execute('INSERT INTO ' + 'tb1 (name) Values ("Jack")')

# 执行批量插入
# values = [(id,'testuser'+str(id)) for id in range(4, 21) ]
# con1.executemany('INSERT INTO '+ TABLE_NAME +' values(%s,%s)' ,values)

con1.close()
conn.close()
```

## 反爬虫以及反反爬虫
###使用fake_useragent模拟浏览器头部信息
基本用法
``` 
# pip install fake-useragent
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

# 模拟不同的浏览器
print(f'Chrome浏览器: {ua.chrome}')
# print(ua.safari)
# print(ua.ie)

# 随机返回头部信息，推荐使用
print(f'随机浏览器: {ua.random}')
```
除了user_agent, Chrome里的network tab任意点击一个html在reqeust header里能找到referer, host, cookies等信息。有时候这些信息也需要模拟。

###同一个session之间所有请求保持cookie
``` 
import requests

# 在同一个 Session 实例发出的所有请求之间保持 cookie
s = requests.Session()

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")

print(r.text)
# '{"cookies": {"sessioncookie": "123456789"}}'

# 会话可以使用上下文管理器
with requests.Session() as s:
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')

```
### 模拟登陆
登陆之后信息会保存在当前会话当中用于后续请求
``` 
import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
'User-Agent' : ua.random,
'Referer' : 'https://accounts.douban.com/passport/login_popup?login_source=anony'
}

s = requests.Session()
# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
form_data = {
'ck':'',
'name':'username',
'password':'password',
'remember':'false',
'ticket':''
}

# 先用get拿到cookies
pre_login = 'https://accounts.douban.com/passport/login'
pre_resp = s.get(pre_login, headers = headers)

response = s.post(login_url, data = form_data, headers = headers)
print(response.text)

# 登陆后可以进行后续的请求
url2 = 'https://accounts.douban.com/passport/setting'

response2 = s.get(url2,headers = headers)
# response3 = newsession.get(url3, headers = headers, cookies = s.cookies)
print(response2.text)
with open('profile.html','w+') as f:
    f.write(response2.text)

```
## WebDriver
### 安装
``` 
pip install selenium

需要安装chrome driver, 和浏览器版本保持一致
http://chromedriver.storage.googleapis.com/index.html
放入python.exe同一个目录下
```

``` 
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    
    browser.get('https://www.douban.com')
    time.sleep(1)

    browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1.click()

    browser.find_element_by_xpath('//*[@id="username"]').send_keys('15055495@qq.com')
    browser.find_element_by_id('password').send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath('//a[contains(@class,"btn-account")]').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()
    
```
打开电影链接，转到短评并翻页
```
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
   
    browser.get('https://movie.douban.com/subject/1292052/')
    time.sleep(1)


    btm1 = browser.find_element_by_xpath('//*[@id="hot-comments"]/a')
    btm1.click()
    time.sleep(5)
    print(browser.page_source)

    next_page = browser.find_element_by_xpath('//div[@id="paginator"]/a')
    next_page.click()

except Exception as e:
    print(e)
# finally:    
#     browser.close()
    
```
用request下载文件
``` 
########## 小文件下载：
import requests
image_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
r = requests.get(image_url)
with open("python_logo.png",'wb') as f:
    f.write(r.content)

############# 大文件下载：
# 如果文件比较大的话，那么下载下来的文件先放在内存中，内存还是比较有压力的。
# 所以为了防止内存不够用的现象出现，我们要想办法把下载的文件分块写到磁盘中。
import requests
file_url = "http://python.xxx.yyy.pdf"
r = requests.get(file_url, stream=True)
with open("python.pdf", "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pdf.write(chunk)
```
### 验证码识别
了解即可
``` 
# 先安装依赖库libpng, jpeg, libtiff, leptonica
# brew install leptonica
# 安装tesseract
# brew install  tesseract
# 与python对接需要安装的包
# pip3 install Pillow
# pip3 install pytesseract

import requests
import os
from PIL import Image
import pytesseract

# 下载图片
# session = requests.session()
# img_url = 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1320441599,4127074888&fm=26&gp=0.jpg'
# agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# headers = {'User-Agent': agent}
# r = session.get(img_url, headers=headers)

# with open('cap.jpg', 'wb') as f:
#     f.write(r.content)

# 打开并显示文件
im = Image.open('cap.jpg')
im.show()

# 灰度图片
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()

# 二值化
threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

out = gray.point(table, '1')
out.save('c_th.jpg')

th = Image.open('c_th.jpg')

#需要安装tesseract并指定路径
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
print(pytesseract.image_to_string(th,lang='chi_sim+eng'))

# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata
```

### 用下载中间件实现代理IP
scrapy crawl httpbin --nolog
此命令可以规避除了ip以外的其他log信息
``` 
{
  "origin": "203.220.167.191"
}
```
设置环境变量

http_proxy='http://52.179.231.206:80' （此处替换为网上找的代理ip)

添加HttpProxyMiddleware, 冒号后面的数字越小优先级越高

scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware

或者可以在middlewares.py里面继承DownloaderMiddleware自己添加功能

### 分布式爬虫
Scrapy 原生不支持分布式，多机之间需要Redis实现队列和管道的共享。

scrapy-redis很好地实现了Scrapy和Redis的集成

主要变化

使用了RedisSpider类替代了spider类
Scheduler的queue有redis实现
item pipeline由Redis实现