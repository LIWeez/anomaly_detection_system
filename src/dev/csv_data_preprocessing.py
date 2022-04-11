# !/usr/bin/python
# -*-coding:utf-8 -*-


import os
import pandas as pd
import numpy as np
import yaml
from time import gmtime, strftime
import shelve

with open('/usr/workspace/config/dev.yml', 'r') as f:
    configArray = yaml.safe_load(f)

def csv_preprocessing(data_path):
    csv_dir = data_path
    df=pd.DataFrame()

    for file_ in os.listdir(csv_dir)[:30]:
        # temp=pd.read_csv('/root/web03_normal_dataset'+'/'+file_, header=None, skiprows=1, sep=";")
        temp=pd.read_csv(csv_dir+'/'+file_) 
        temp['Time'] = pd.to_datetime(temp.Time, format='%Y-%m-%d %H:%M:%S')
        temp['Time'] = temp['Time'].dt.tz_localize('UTC')
        temp['Time'] = pd.to_datetime(temp['Time']).dt.tz_convert('Asia/Taipei')
        temp['Time'] = temp['Time'].dt.tz_localize(None)
        temp.index = pd.to_datetime(temp.Time, format = '%m/%d/%Y')
        # how = sum when dataset time is 1m
        temp = temp.resample('1min').mean()
        # temp = temp.fillna(0)
        temp = temp.fillna(method='pad')
        temp = temp.fillna(method='backfill')
        temp.columns.name = None
        df=pd.concat([df,temp],ignore_index=False)

    df = df.sort_index()
    df.to_csv('temp_single_file.csv',index=True)

def get_singma(dataset):
    singma = []
    for i in range(24):
        for j in range(60):
            time_mask = (dataset.index.hour == i) & \
                (dataset.index.minute == j)
            # temp_point = np.percentile(normal_dataset[time_mask], 50, axis=0)
            temp_point = np.mean(dataset[time_mask])
            singma.append(temp_point[0])
    return singma

def get_stds(dataset):
    stds = []
    for i in range(24):
        for j in range(60):
            time_mask = (dataset.index.hour == i) & \
                (dataset.index.minute == j)
            # temp_point = np.percentile(normal_dataset[time_mask], 50, axis=0)
            temp_point = np.std(dataset[time_mask], ddof=0)
            stds.append(temp_point[0])
    return stds


if __name__ == '__main__':
    for dashboard in configArray:
        for machine in configArray[dashboard]:
            for sub_dashboard in configArray[dashboard][machine]:
                for model_index in range(len(configArray[dashboard][machine][sub_dashboard]['model'])):
                    data_file = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['data_path']
                    csv_preprocessing(data_file)
                    
                    normal_dataset = pd.read_csv(
                        'temp_single_file.csv', parse_dates=True, index_col='Time'
                    )

                    algorithm = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['algorithm']

                    ## 這裡是我的實驗區塊，主要是寫IF script去判斷選擇要用模型訓練
                    if algorithm == 'average_of_the_historical_data':
                        singma = get_singma(normal_dataset)
                        stds = get_stds(normal_dataset)

                        # 建立shelf物件，儲存訓練好的模型
                        data_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['model_path']
                        shelf_name = strftime("%Y%m%d%H%M%S", gmtime())

                        shelf_path = "%s/%s.shelve" % (data_path, shelf_name)

                        model = shelve.open(shelf_path)
                        model['singma'] = singma
                        model['stds'] = stds

                        model.close()

                    elif algorithm == 'moving_maximum_of_the_historical_data':
                        normal_dataset = normal_dataset.rolling(window=8, min_periods=1, center=True, axis=0).max()

                        singma = get_singma(normal_dataset)
                        stds = get_stds(normal_dataset)

                        # 建立shelf物件，儲存訓練好的模型
                        data_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['model_path']
                        shelf_name = strftime("%Y%m%d%H%M%S", gmtime())

                        shelf_path = "%s/%s.shelve" % (data_path, shelf_name)

                        model = shelve.open(shelf_path)
                        model['singma'] = singma
                        model['stds'] = stds

                        model.close()

                    elif algorithm == 'average_rate_of_change_of_the_historical_data':
                        normal_dataset = normal_dataset.pct_change()
                        normal_dataset = normal_dataset.dropna()

                        singma = get_singma(normal_dataset)
                        stds = get_stds(normal_dataset)

                        # 建立shelf物件，儲存訓練好的模型
                        data_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['model_path']
                        shelf_name = strftime("%Y%m%d%H%M%S", gmtime())

                        shelf_path = "%s/%s.shelve" % (data_path, shelf_name)

                        model = shelve.open(shelf_path)
                        model['singma'] = singma
                        model['stds'] = stds

                        model.close()
                        
                    elif algorithm == 'moving_maximum_and_minimum_of_the_historical_data':
                        temp_normal_dataset = normal_dataset.copy()
                        normal_dataset = normal_dataset.rolling(window=5, min_periods=1, center=True, axis=0).max()

                        singma = get_singma(normal_dataset)
                        stds = get_stds(normal_dataset)

                        # 建立shelf物件，儲存訓練好的模型
                        data_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['model_path']
                        shelf_name = strftime("%Y%m%d%H%M%S", gmtime())

                        shelf_path = "%s/%s.shelve" % (data_path, shelf_name)

                        model = shelve.open(shelf_path)
                        model['singma'] = singma
                        model['stds'] = stds
                        model['max_singma'] = singma
                        model['max_stds'] = stds

                        temp_normal_dataset = temp_normal_dataset.rolling(window=5, min_periods=1, center=True, axis=0).min()
                        singma = get_singma(temp_normal_dataset)
                        stds = get_stds(temp_normal_dataset)

                        model['min_singma'] = singma
                        model['min_stds'] = stds

                        model.close()




os.remove("/usr/workspace/temp_single_file.csv")













