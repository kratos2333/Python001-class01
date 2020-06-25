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
### 注意点
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

### 注意点
beautifulsoup的findall会找到所有相关元素，比如bs_info.find_all('div', attrs={'class': 'a'})会找到所有class带hd的div元素，也就是说class="a b"的div元素也会被找到

## 3. 使用lxml通过xpath解析页面
单一元素的xpath可以通过chrome浏览器devtool里右键该元素获取。
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

4. spiders(需要修改）- 相当于bs4 和 lxml。 用于从特定网页中提取需要的信息，用户也可以用从中提取出链接，让Scrapy继续抓取下一个页面

5. item pipelines(需要修改）- 项目管道负责处理爬虫从网页中抽取的实体。主要功能是持久化实体，验证实体的有效性，清除不需要的信息。（比如存入csv/txt/MySql等）

6. downloader middlewares （一般不用修改）

7. spider middlewares（一般不用修改）

### 安装初始化
安装包：pip install scrapy

初始化项目：scrapy startproject projectName

新建一个spider: scrapy genspider spiderName realdomain
