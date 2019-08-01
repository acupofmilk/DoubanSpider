'''
模拟登录豆瓣，进行一系列操作
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class LoginDouBan():
    def __init__(self):
        self.login_url = "https://accounts.douban.com/j/mobile/login/basic"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "Referer": "https://accounts.douban.com/passport/login?source=main",
        }
        self.login_from_data = {
            'name': 'your_username',
            'password': 'your_password',
            'remember': 'false'
        }
        self.s = requests.session()

    def login(self):
        try:
            r = self.s.post(self.login_url, headers=self.headers, data=self.login_from_data)
            r.encoding = r.apparent_encoding
            r.raise_for_status()  # 主动抛出异常
        except:
            print("登录失败")

    def user_page(self) -> requests.models.Response:  # 登录到个人页面
        url = "https://www.douban.com/mine/"
        page = self.s.get(url, headers=self.headers)
        return page

    def search(self) -> pd.core.frame.DataFrame :
        terms = input("输入要查找内容： ")
        url = "https://www.douban.com/search"
        params = {
            'source': 'suggest',
            'q': terms
        }
        try:
            r = self.s.get(url, params=params, headers=self.headers)
            r.raise_for_status()
        except:
            print("搜索失败！")
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html5lib")
        results = soup.select('.search-result .result-list')[0].select('.result .title')

        df = pd.DataFrame(columns=['type', 'name', 'link'])

        for result in results:
            type = result.find('span').text
            name = result.find('a').text
            link = result.find('a')['href']
            series = pd.Series(data=[type, name, link], index=['type', 'name', 'link'])
            df = df.append(series, ignore_index=True)
        return df

    def run(self):
        self.login()
        df = self.search()
        return df




df = LoginDouBan().run()

