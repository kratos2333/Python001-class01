# 第一周 学习笔记
## 1. requests and urllib
请求页面常用的库投urllib以及requests. urllib是标准库里自带的，使用的时候需要编解码没有requests方便，并不推荐使用
### 基本用法

```
import requests
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent':user_agent}
myurl = 'https://movie.douban.com/top250'
response = requests.get(myurl,headers=header)

print(response.text)
print(f'返回码是: {response.status_code}')
```
### 拓展
 在进行页面请求时需要传入header，以模拟一般浏览器。对于豆瓣而言只需要加入user_agent即可，但是对于有些网站例如猫眼。需要添加更多信息
其中COOKIES是为了绕过验证页面，需要找到cookies的uuid,可以利用chrome浏览器application标签页进行查看
```
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Accept': "*/*",
    'Accept-Encoding': 'gazip, deflate, br',
    'Accept-Language': 'en-AU,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,la;q=0.6',
    'Content-Type': 'text/plain',
    'Connection': 'keep-alive',
    'Origin': 'https://maoyan.com',
    'Referer': 'https://maoyan.com/films?showType=3',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'COOKIES': '15BB0FD0B69311EA9B3075693A212BAFAD6D26C3EC524AC9AF0FB5604380B7E5'
}
```

## 2. 使用beautifulsoup解析网页
用requests获取html页面之后用beautifulsoup可以对页面元素进行分析处理。

缺点：纯python实现，整个页面搜索效率较低
###基本用法
https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

对于单一数据可以直接通过a.b.c的方式进行获取。比如bs_info.title.text可以获取页面的title信息

以下代码片段示范了如何找到带有相同特征的元素
``` 
import requests
from bs4 import BeautifulSoup as bs
...
response = requests.get(myurl,headers=header)
bs_info = bs(response.text, 'html.parser')

# Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
for tags in bs_info.find_all('div', attrs={'class': 'hd'}):
    for atag in tags.find_all('a',):
        print(atag.get('href'))
        # 获取所有链接
        print(atag.find('span',).text)
        # 获取电影名字
```
带翻页功能
``` 
import requests
from bs4 import BeautifulSoup as bs

# Python 使用def定义函数，myurl是函数的参数
def get_url_name(myurl):
    ...
    
    # Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
    for tags in bs_info.find_all('div', attrs={'class': 'hd'}):
        for atag in tags.find_all('a',):
            # 获取所有链接
            print(atag.get('href'))
            # 获取电影名字
            print(atag.find('span',).text)

# 生成包含所有页面的元组
urls = tuple(f'https://movie.douban.com/top250?start={ page * 25 }&filter=' for page in range(10))

# 控制请求的频率，引入了time模块
from time import sleep
sleep(10)
for page in urls:
    get_url_name(page)
    sleep(5)
```

### 拓展
beautifulsoup的findall会找到所有相关元素，比如bs_info.find_all('div', attrs={'class': 'a'})会找到所有class带hd的div元素，也就是说class="a b"的div元素也会被找到

## 3. 使用lxml通过xpath解析页面
单一元素的xpath可以通过chrome浏览器devtool里右键该元素获取。

优点： C实现，效率比bs4快了不止10倍
### 基本用法
``` 
//      从头开直到找到满足条件的元素 (.xpath('//div[@class="hd"]'))
./      从当前路径开始往下找
../     从父节点开始找
@       获取元素的attribute (link = movie.xpath('./a/@href'))
/text() 当前元素的文字
```
爬取页面基本信息
``` 
import requests
import lxml.etree
...

# xml化处理
selector = lxml.etree.HTML(response.text)

# 电影名称
film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')
print(f'电影名称: {film_name}')

# 上映日期
plan_date = selector.xpath('//*[@id="info"]/span[10]/text()')
print(f'上映日期: {plan_date}')

# 评分
rating = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
print(f'评分：{rating}')
```

## 4. Scrapy框架
https://docs.scrapy.org/en/latest/topics/architecture.html

### 核心组件
1. engine（无需修改，框架已写好）- 指挥其他组件协同工作

2. scheduler（无需修改，框架已写好）- 将引擎发来的请求进行先后排序，压入队列，同时去除重复的请求。

3. downloader(无需修改，框架已写好) - 用于下载网页内容，并返回给爬虫 相当于requests 库

4. spiders(需要修改）- 相当于bs4 和 lxml。 用于从特定网页中提取需要的信息，用户也可以用从中提取出链接，让Scrapy继续抓取下一个页面。
当spider parse完之后可以选择继续向scheduler调度器发起一个Request或者是返回item

5. item pipelines(需要修改）- 项目管道负责处理爬虫从网页中抽取的实体。主要功能是持久化实体，验证实体的有效性，清除不需要的信息。（比如存入csv/txt/MySql等）

6. downloader middlewares （一般不用修改）

7. spider middlewares（一般不用修改）

### 安装初始化&一些命令
安装包：pip install scrapy

初始化项目：scrapy startproject projectName

新建一个spider: scrapy genspider spiderName realdomain

爬取： scrapy crawl spiderName
### settings.py
USER_AGENT = 'doubanmovie (+http://www.yourdomain.com)' 
一般来说只要打开这个设置就行了，scrapy会根据start_url获取相应头信息

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'doubanmovie.pipelines.DoubanmoviePipeline': 300,
}

### spider.py
指定爬取范围： allowed_domains = ['movie.douban.com']

开始连接： start_urls = ['https://movie.douban.com/top250'], 即便是用了start_requests函数也要加start_url因为异步框架twisted需要

默认爬取函数： def parse(self, response) 如果只设置该函数response会从start_url获取

初始化函数：  def start_requests(self) 

**scrapy + bs4实现翻页并且进入详细页面获取信息**
``` 
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from doubanmovie.items import DoubanmovieItem


class DoubanSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # 起始URL列表
    start_urls = ['https://movie.douban.com/top250']

#   注释默认的parse函数
#   def parse(self, response):
#        pass


    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        for i in range(0, 10):
            url = f'https://movie.douban.com/top250?start={i*25}'
            yield scrapy.Request(url=url, callback=self.parse)
            # url 请求访问的网址
            # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
            # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数

    # 解析函数
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        title_list = soup.find_all('div', attrs={'class': 'hd'})
        #for i in range(len(title_list)):
        # 在Python中应该这样写
        for i in title_list:
            # 在items.py定义
            item = DoubanmovieItem()
            title = i.find('a').find('span',).text
            link = i.find('a').get('href')
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    # 解析具体页面
    def parse2(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', attrs={'class': 'related-info'}).get_text().strip()
        item['content'] = content
        yield item
```
**scrapy + scrapy xpath (from scrapy.selector import Selector)**
``` 
# -*- coding: utf-8 -*-
import scrapy
from doubanmovie.items import DoubanmovieItem
from scrapy.selector import Selector

class DoubanSpider(scrapy.Spider):
    ...

    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        # for i in range(0, 10):
            i=0
            url = f'https://movie.douban.com/top250?start={i*25}'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
            # url 请求访问的网址
            # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
            # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数

    # 解析函数
    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="hd"]')
        for movie in movies:
            # 路径使用 / .  .. 不同的含义　
            title = movie.xpath('./a/span/text()')
            link = movie.xpath('./a/@href')
            print('-----------')
            print(title)
            print(link)
            print('-----------')
            print(title.extract())
            print(link.extract())
            print(title.extract_first())
            print(link.extract_first())
            print(title.extract_first().strip())
            print(link.extract_first().strip())  
```

### items.py
相当于java中的DAO
``` 
import scrapy
class DoubanmovieItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
```
###  pipeline.py

``` 
# -*- coding: utf-8 -*-
# 注册到settings.py文件的ITEM_PIPELINES中，激活组件
class DoubanmoviePipeline:
#    def process_item(self, item, spider):
#        return item

    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        content = item['content']
        output = f'|{title}|\t|{link}|\t|{content}|\n\n'
        with open('./doubanmovie.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item
```
### 拓展
settings.py可以设置随机选取USER_AGENT以更好的模拟浏览器
``` 
USER_AGENT_LIST=[
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
import random
USER_AGENT = random.choice(USER_AGENT_LIST)
```
Debug Scrappy

根目录中放入debug.py
``` 
from scrapy.cmdline import execute
execute()
```
run setting设置对debug.py修改配置添加parameter 
crawl spiderName就可以debebug了