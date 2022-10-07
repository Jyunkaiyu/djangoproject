import pandas as pd
import lxml
import requests
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class Website(ABC):
 
    def __init__(self, gpu_name1):
        self.name1 = gpu_name1  # 城市名稱屬性
    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass

class gpuchallenge(Website):
    def scrape(self):
        result = []  # 回傳結果
        if self.name1:

            df = pd.read_csv('.\myapp\gpu_rank.csv', encoding='big5')
            qs=self.name1
            #qs2=self.name2
            #df2 = np.array(df)
            namlst = []
            numlst = []
            for i in range(len(df['gpu'])):
                if qs in df['gpu'][i]:
                    namlst.append(df['gpu'][i])
                    numlst.append(df['gpu_point'][i])

                    ans1=df['gpu_point'][i]
            strans1 = str(ans1)

            for i in range(len(namlst)):

                a=namlst[i]
                b=numlst[i]

                result.append(
                    dict(gpuone=a  , score_one=b))

            
 
            return result


