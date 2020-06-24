# -*- coding: utf-8 -*-
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

'''
作业一：
安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
'''


def crawl_maoyan():
    #########################################################################
    # local test only
    # local_html_path = 'C:\\Users\\kevin\\OneDrive\\Desktop\\mapyan.html'
    # htmlfile = open(local_html_path, 'r', encoding='utf-8')
    # htmlhandle = htmlfile.read()
    # bs_finder = bs(htmlhandle, 'lxml')
    #########################################################################

    # Fetch the html contents from REQUEST_URL
    REQUEST_URL = 'http://maoyan.com/films?showType=3'
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
        'COOKIES': '9BC88680B61511EA801551553EAD9849CFABF5DDC2EE41B891FB0381008CF57B'
    }

    response = requests.get(REQUEST_URL, headers=HEADER)

    # Parse the html content
    bs_finder = bs(response.text, 'html.parser')

    movie_dict = {'movie_title': [], 'movie_type': [], 'release_date': []}
    # first 10 movies
    for movies in bs_finder.findAll('div', attrs={'class': 'movie-item film-channel'})[:10]:

        # Get movie title, type, release_date
        info_list = movies.findAll('div', attrs={'class': 'movie-hover-title'})
        movie_title = info_list[0].get('title')
        movie_type = info_list[1].text.strip().split('\n')[1].strip()
        release_date = info_list[3].text.strip().split('\n')[1].strip()

        movie_dict['movie_title'].append(movie_title)
        movie_dict['movie_type'].append(movie_type)
        movie_dict['release_date'].append(release_date)

    return movie_dict

if __name__ == '__main__':
    movieDF = pd.DataFrame(data=crawl_maoyan())
    movieDF.to_csv('./movie.csv', sep='\t', encoding='utf-8', index=False, header=True)