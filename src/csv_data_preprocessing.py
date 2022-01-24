# !/usr/bin/python
# -*-coding:utf-8 -*-


import os
import pandas as pd
import numpy as np
import yaml

grafana_csv_dir = '/root/api_model_system/api-anomaly-detection/data_set/no_maintenance'
# grafana_csv_dir = '/root/api_model_system/api-anomaly-detection/data_set/1115_no_maintanece'
# grafana_csv_dir = '/root/api_model_system/api-anomaly-detection/data_set/temp/csvCreactor'
df=pd.DataFrame()
for file_ in os.listdir(grafana_csv_dir):
    # temp=pd.read_csv('/root/web03_normal_dataset'+'/'+file_, header=None, skiprows=1, sep=";")
    temp=pd.read_csv(grafana_csv_dir+'/'+file_, sep=";") 
    temp['Time'] = pd.to_datetime(temp['Time']).dt.tz_convert('Asia/Taipei')
    temp['Time'] = temp['Time'].dt.tz_localize(None)
    temp.index = pd.to_datetime(temp.Time, format = '%m/%d/%Y')
    # how = sum when dataset time is 1m
    temp = temp.resample('1min', how='mean')
    # temp = temp.fillna(0)
    temp = temp.fillna(method='pad')
    temp = temp.fillna(method='backfill')
    temp.columns.name = None
    df=pd.concat([df,temp],ignore_index=False)



df = df.sort_index()

df.to_csv('single_file.csv',index=True)
print('Success!')
