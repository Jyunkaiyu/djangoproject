from this import d
import pandas as pd
import lxml
import requests
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class Website(ABC):
 
    def __init__(self, cpu_name1,cpu_name2):
        self.name1 = cpu_name1  # 城市名稱屬性
        self.name2 = cpu_name2
    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass

class cpuchallenge(Website):
    def scrape(self):
        result = []  # 回傳結果
        if self.name1:

            df = pd.read_csv('.\myapp\cpu_rank.csv', encoding='big5')
            qs=self.name1
            qs2=self.name2
            #df2 = np.array(df)
            namlst = []
            numlst = []
            namlst2 = []
            numlst2 = []
            for i in range(len(df['cpu'])):
                if qs in df['cpu'][i]:
                    namlst.append(df['cpu'][i])
                    numlst.append(df['cpu_point'][i])
                    ans1=df['cpu_point'][i]

                if qs2 in df['cpu'][i]:
                    namlst2.append(df['cpu'][i])
                    numlst2.append(df['cpu_point'][i])
                    ans2=df['cpu_point'][i]
            for i in range(len(namlst)):

                a=namlst[i]
                b=numlst[i]
                c=namlst2[i]
                d=numlst2[i]
                if b>d:
                    e = a+" is better cpu than "+c
                else:
                    e = c+" is better cpu than "+a

                result.append(
                    dict(cpuone=a  , score_one=b , cputwo=c , score_two=d , cpuwinner=e))

            
 
            return result


