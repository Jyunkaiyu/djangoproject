from abc import ABC, abstractmethod
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
from datetime import datetime

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
      'Cookie':'uuid=3bfbeb56-9f3e-4d0d-cbe3-260b14154476; cityDomain=gy; ganji_uuid=2943330065231720816366; lg=1; antipas=z6683504k93003WPO325643r3; clueSourceCode=%2A%2300; user_city_id=36; sessionid=c1cf6d12-f864-40c1-be6a-689466580011; close_finance_popup=2020-07-27; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%223bfbeb56-9f3e-4d0d-cbe3-260b14154476%22%2C%22ca_city%22%3A%22gy%22%2C%22sessionid%22%3A%22c1cf6d12-f864-40c1-be6a-689466580011%22%7D; Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f=1595389723,1595834426,1595834461; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; preTime=%7B%22last%22%3A1595835397%2C%22this%22%3A1595389721%2C%22pre%22%3A1595389721%7D; Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f=1595835398'}


class Website(ABC):
 
    def __init__(self, city_name):
        self.name = city_name  # 城市名稱屬性
 
    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass

class pchome(Website):
 
    def scrape(self):
 
        result = []  # 回傳結果

        if self.name:
            headers = {'cookie': 'ECC=GoogleBot',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

            prodids = []
            propris = []
            proid = []
            for page in list(range(1, 6)):
                url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page={}&sort=sale/dc'.format(self.name, page)
                resp = requests.get(url,headers=headers)
                for prodid in resp.json()['prods']:
                    prodids.append(prodid['name'])
                    propris.append(prodid['price'])
                    proid.append(prodid['Id'])


            for i in range(len(prodids)):
                a=prodids[i]
                b=propris[i]
                c=proid[i]
                d="https://24h.pchome.com.tw/prod/{}".format(c)

                booking_date=0
                star = 0

                result.append(
                    dict(title=a, link=d, price=b, booking_date=booking_date, star=star, source="https://buzzorange.com/techorange/2018/02/09/makes-pchome-great-again/"))
 
        return result

