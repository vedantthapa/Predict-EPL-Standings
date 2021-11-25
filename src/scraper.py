#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   scraper.py
@Time    :   2021/10/31 13:54:53
@Author  :   Vedant Thapa 
@Contact :   thapavedant@gmail.com
'''


from tqdm import tqdm
import pandas as pd
import warnings
import sys


warnings.filterwarnings(action='ignore')

year_iter1 = [i for i in range(2005, 2020)]
year_iter2 = [i for i in range(2006, 2021)]

epl = pd.DataFrame()

values = list(zip(year_iter1, year_iter2))
with tqdm(total=len(values), file=sys.stdout) as pbar:
    for i, j in values:
        season = str(i)[-2:] + str(j)[-2:]
        pbar.set_description(f"processing {season}")
        pbar.update()

        try:
            df_ = pd.read_csv(f'https://www.football-data.co.uk/mmz4281/{season}/E0.csv', error_bad_lines=False)
            df_.insert(1, 'season', season)
            df_ = df_.dropna(how='all')
            epl = epl.append(df_)
        except:
            print(f'Error processing season: {season}')

if all(epl.groupby('season').Date.count() == 380):
    print('Scraped successfully without errors')
    epl.reset_index(drop=True).to_csv('../data/epl_05-20.csv', index=False)
