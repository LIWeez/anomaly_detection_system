# !/usr/bin/python
# -*-coding:utf-8 -*-


import os
import pandas as pd
import numpy as np
import yaml
from time import gmtime, strftime
import shelve

with open('/usr/workspace/config/prod.yml', 'r') as f:
    configArray = yaml.safe_load(f)

def csv_preprocessing(data_path):
    csv_dir = data_path
    df=pd.DataFrame()

    for file_ in os.listdir(csv_dir):
        # temp=pd.read_csv('/root/web03_normal_dataset'+'/'+file_, header=None, skiprows=1, sep=";")
        temp=pd.read_csv(csv_dir+'/'+file_, sep=";") 
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

def get_singma():
    singma = []
    for i in range(24):
        for j in range(60):
            time_mask = (normal_dataset.index.hour == i) & \
                (normal_dataset.index.minute == j)
            # temp_point = np.percentile(normal_dataset[time_mask], 50, axis=0)
            temp_point = np.mean(normal_dataset[time_mask])
            singma.append(temp_point[0])
    return singma

def get_stds():
    stds = []
    for i in range(24):
        for j in range(60):
            time_mask = (normal_dataset.index.hour == i) & \
                (normal_dataset.index.minute == j)
            # temp_point = np.percentile(normal_dataset[time_mask], 50, axis=0)
            temp_point = np.std(normal_dataset[time_mask], ddof=0)
            stds.append(temp_point[0])


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

                    singma = get_singma()
                    stds = get_stds()


                    # 建立shelf物件，儲存訓練好的模型
                    data_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['model_path']
                    shelf_name = strftime("%Y%m%d%H%M%S", gmtime())

                    shelf_path = "%s/%s.shelve" % (data_path, shelf_name)

                    model = shelve.open(shelf_path)
                    model['singma'] = singma
                    model['stds'] = stds

                    model.close()










                    


                














