# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 11:12:38 2022

@author: Malte Fritz
"""

from os import listdir
from os.path import isfile, join
import json
from datetime import datetime
import pandas as pd

mypath = (
    r'C:\Users\Malte Fritz\Documents\Malte\98_Sontiges\Sonstiges\Fußball'
    + r'\Individuelles Training\export-20220729-000\Sport-sessions'
    )

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

df = pd.DataFrame(columns=['date', 'distance', 'run time', 'pace', 'speed'])
df.set_index('date', inplace=True)

for session in onlyfiles:
    with open(join(mypath, session), 'r', encoding='utf-8') as file:
        data = json.load(file)

    date = datetime.fromtimestamp(data['start_time'] / 1000).date()
    df.loc[date, 'distance'] = data['distance'] / 1000
    df.loc[date, 'run time'] = round(data['duration'] / 1000, 0)
    df.loc[date, 'pace'] = round(data['duration_per_km'] / 60000, 2)
    df.loc[date, 'speed'] = round(data['average_speed'], 2)

df.to_csv('export_adidas_stats.csv', sep=';', index='date')
