#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import time
import os
import yaml

# 測試用
# import sys

import math
import glob
import shelve
import pandas as pd
import numpy as np
import seaborn as sns
import telegram
from telegram import InputMediaPhoto
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

with open('/usr/workspace/config/dev.yml', 'r') as f:
    configArray = yaml.safe_load(f)

def login(drive,username,passwd):
    input = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div/div[2]/div/div[1]/form/div[1]/div[2]/div/div/input')
    input.send_keys(username)
    print('grafana輸入帳號中⋯')
    input = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div/div[2]/div/div[1]/form/div[2]/div[2]/div/div/input')
    input.send_keys(passwd)
    print('grafana輸入密碼中⋯')

    input.send_keys(Keys.ENTER)
    drive.implicitly_wait(3000)
    print('登入完成')
    # skip changing password  
    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div[2]/button').click()

def download_csv_file(url):    
    driver.get(url)

    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[%s]/div/div[1]/div/div[1]/div/div" % (configArray[dashboard][machine][sub_dashboard]['grafana']['div_id'])).click()
    # driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div').click()

    modal_box_popping_up = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[%s]/div/div[1]/div/div[1]/div/div/div[2]/div/ul/li[5]/a" % (configArray[dashboard][machine][sub_dashboard]['grafana']['div_id']))
    # modal_box_popping_up = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div/ul/li[5]/a')
    ActionChains(driver).move_to_element(modal_box_popping_up).perform()

    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[%s]/div/div[1]/div/div[1]/div/div/div[2]/div/ul/li[5]/ul/li[1]/a" % (configArray[dashboard][machine][sub_dashboard]['grafana']['div_id'])).click()
    # driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div/ul/li[5]/ul/li[1]/a').click()
 
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/button'))).click()
    except TimeoutException:
        print("ERROR: modal box does not pop up.")

def Classifier(datetime, classify_method):
    print("datetime.isoweekday():" + str(datetime.isoweekday()))
    print("classify_method:" +str(classify_method))
    if classify_method == 'check_maintanece':
        if datetime.isoweekday() != 3:
            return False

        week_number = datetime.isocalendar()[1]
        # 今年2022年的第5週是春節，所以維護週遞延一週
        if datetime.isocalendar()[1] >= 5:
            week_number += 1
        if datetime.isocalendar()[1] >= 38:
            week_number += 1

        if week_number % 2 == 1 :
            return True
        return False

    elif classify_method == 'update_days':
        if datetime.isoweekday() == 2 or datetime.isoweekday() == 5:
            return True

    elif classify_method == 'normal':
        return True


if __name__ == '__main__':
    username="admin"  
    passwd="admin" 
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    
    print('進入grafana網頁')
    driver.get("http://grafana.dev3/")
    login(driver, username, passwd)  

    for ndays in range(27, 20, -1):
        # the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(hours=-8, seconds=-1)
        the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(hours=-(ndays*24+8), seconds=-1)
        print("開始測試"+str(ndays))

        for dashboard in configArray:
            for machine in configArray[dashboard]:
                for sub_dashboard in configArray[dashboard][machine]:
                    # 下載該面版前一天的資料
                    file_path = ''

                    start_timestemp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000-86400000+1000)
                    end_timestamp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000)

                    # 根據資料的日期，決定要用哪一個資料模型判斷異常
                    # 這一天的監控資料符合目前指針所指的model要用的資料嗎，如果是的話就返回True。
                    for model_index in range(len(configArray[dashboard][machine][sub_dashboard]['model'])):
                        model_path_status = False
                        model_path_status = Classifier(the_day_before_datetime, configArray[dashboard][machine][sub_dashboard]['model'][model_index]['classify_method'])
                        print("驗證方法︰"+str(configArray[dashboard][machine][sub_dashboard]['model'][model_index]['classify_method']))
                        if model_path_status == True:
                            model_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['model_path']
                            algorithm = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['algorithm']
                            print("驗證狀態︰成功")
                            break
                        print("驗證狀態︰失敗")

                    if algorithm == 'average_rate_of_change_of_the_historical_data':
                        start_timestemp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000-86400000)
                    
                    url = "%s&from=%s&to=%s" % (configArray[dashboard][machine][sub_dashboard]['grafana']['url'], start_timestemp, end_timestamp)
                    print(url)
                    print('下載csv檔案')
                    download_status = False

                    # 檢查檔案有無下載完全
                    while download_status == False:
                        size = 0
                        download_csv_file(url)
                        time.sleep(40/1000)
                        try:
                            # 因開發站使用的grafana下載下來的csv檔不再叫做grafana.csv，所以需要透過其他的方式來獲取下載的檔案
                            lists = os.listdir('/usr/workspace')
                            lists.sort(key=lambda fn:os.path.getmtime('/usr/workspace' + "/" + fn))
                            file_new = os.path.join('/usr/workspace',lists[-1])
                            print(file_new)
                            shutil.move(file_new, 'grafana_data_export.csv')
                            size = os.path.getsize('grafana_data_export.csv')
                        except Exception as e:
                            print('download error.')
                        if size > 100:
                            download_status = True




                    # 讀取最新的shelf，並還原成list模型。
                    list_of_shelves = glob.glob("%s/*" % (model_path))
                    latest_shelf = max(list_of_shelves, key=os.path.getctime)

                    model = shelve.open(latest_shelf)

                    # test
                    print(latest_shelf)
                    
                    np_singma = np.array(model['singma'])
                    np_stds = np.array(model['stds'])

                    # 讀取config目錄中的yml檔中模型的閾值
                    threshold = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['threshold']

                    ##接下來我應該要如何取得要檢測的資料？目前就我來看
                    ##即使只有一天的資料也需要csv.proces，才能被pandas正確的索引出來的。

                    # 預處理要異常判斷的資料，這裡會將原本gmt+0的時區改成gmt+8的時區，因開發站使用的grafana下載下來的csv檔不再叫做grafana.csv，所以需要透過其他的方式來獲取下載的檔案

                    lists = os.listdir('/usr/workspace')
                    lists.sort(key=lambda fn:os.path.getmtime('/usr/workspace' + "/" + fn))
                    file_new = os.path.join('/usr/workspace',lists[-1])
                    
                    detect_data=pd.read_csv(file_new) 
                    detect_data['Time'] = pd.to_datetime(detect_data.Time, format='%Y-%m-%d %H:%M:%S')
                    detect_data['Time'] = detect_data['Time'].dt.tz_localize('UTC')
                    detect_data['Time'] = pd.to_datetime(detect_data['Time']).dt.tz_convert('Asia/Taipei')
                    detect_data['Time'] = detect_data['Time'].dt.tz_localize(None)
                    detect_data.index = pd.to_datetime(detect_data.Time, format = '%m/%d/%Y')

                    # 更改欄位名稱
                    columns_list = detect_data.columns.values.tolist()
                    detect_data.rename(columns = {columns_list[1]:"Value"}, inplace = True)

                    detect_data = detect_data.resample('1min').mean()
                    tedetect_datamp = detect_data.fillna(method='pad')
                    detect_data = detect_data.fillna(method='backfill')

                    # 建立模型計算出來的平均數物件
                    df_singma = pd.DataFrame(
                        model['singma'], columns=['Value'])

                    ## 這裡是我的實驗區塊，主要是寫IF script去判斷選擇要用模型訓練
                    if algorithm == 'average_of_the_historical_data':
                        # 判斷異常。
                        anomalies = []

                        # test
                        # detect_data.iloc[240] = 240

                        df_singma.index = detect_data.index
                        for i in range(24):
                            for j in range(60):
                                time_mask = (detect_data.index.hour == i) & \
                                            (detect_data.index.minute == j)
                                time_mask_np = i*60+j

                                if detect_data.values[time_mask][0][0] > np_singma[time_mask_np]+np_stds[time_mask_np] * threshold:
                                    anomaly = 2
                                elif detect_data.values[time_mask][0][0] < np_singma[time_mask_np]-np_stds[time_mask_np] * threshold:
                                    anomaly = 1
                                else:
                                    anomaly = 0
                                anomalies.append(anomaly)

                    elif algorithm == 'moving_maximum_of_the_historical_data':
                        # 判斷異常。
                        anomalies = []

                        df_singma.index = detect_data.index
                        for i in range(24):
                            for j in range(60):
                                time_mask = (detect_data.index.hour == i) & \
                                            (detect_data.index.minute == j)
                                time_mask_np = i*60+j

                                if detect_data.values[time_mask][0][0] > np_singma[time_mask_np]+np_stds[time_mask_np] * threshold:
                                    anomaly = 2
                                elif detect_data.values[time_mask][0][0] < np_singma[time_mask_np]-np_stds[time_mask_np] * (threshold * 2):
                                    anomaly = 1
                                else:
                                    anomaly = 0
                                anomalies.append(anomaly)

                    elif algorithm == 'average_rate_of_change_of_the_historical_data':
                        # 判斷異常。
                        anomalies = []

                        # 因爲是變化率模型，所以需要使用pd的函數將原本單純的數值運算成變化率
                        detect_data = detect_data.pct_change()
                        detect_data = detect_data.iloc[1: , :]
                        print(detect_data.shape)

                        df_singma.index = detect_data.index

                        for i in range(24):
                            for j in range(60):
                                time_mask = (detect_data.index.hour == i) & \
                                            (detect_data.index.minute == j)
                                time_mask_np = i*60+j

                                if detect_data.values[time_mask][0][0] > np_singma[time_mask_np]+np_stds[time_mask_np] * threshold:
                                    anomaly = 2
                                elif detect_data.values[time_mask][0][0] < np_singma[time_mask_np]-np_stds[time_mask_np] * (threshold * 2):
                                    anomaly = 1
                                else:
                                    anomaly = 0
                                anomalies.append(anomaly)


                    elif algorithm == 'moving_maximum_and_minimum_of_the_historical_data':
                        # 判斷異常。
                        anomalies = []

                        max_np_singma = np.array(model['max_singma'])
                        max_np_stds = np.array(model['max_stds'])
                        min_np_singma = np.array(model['min_singma'])
                        min_np_stds = np.array(model['min_stds'])

                        max_df_singma = pd.DataFrame(
                        model['max_singma'], columns=['Value'])
                        min_df_singma = pd.DataFrame(
                        model['min_singma'], columns=['Value'])

                        max_df_singma.index = detect_data.index
                        min_df_singma.index = detect_data.index
   
                        # test
                        # detect_data.iloc[240] = 240

                        for i in range(24):
                            for j in range(60):
                                time_mask = (detect_data.index.hour == i) & \
                                            (detect_data.index.minute == j)
                                time_mask_np = i*60+j

                                if detect_data.values[time_mask][0][0] > max_np_singma[time_mask_np]+max_np_stds[time_mask_np] * threshold:
                                    anomaly = 2
                                elif detect_data.values[time_mask][0][0] < min_np_singma[time_mask_np]-min_np_stds[time_mask_np] * threshold:
                                    anomaly = 1
                                else:
                                    anomaly = 0
                                anomalies.append(anomaly)

                                # if detect_data.values[time_mask][0][0] > np_singma[time_mask_np]+np_stds[time_mask_np] * threshold:
                                #     anomaly = 2
                                # elif detect_data.values[time_mask][0][0] < np_singma[time_mask_np]-np_stds[time_mask_np] * threshold:
                                #     anomaly = 1
                                # else:
                                #     anomaly = 0
                                # anomalies.append(anomaly)

                    anomalies = np.array(anomalies)   

                    #如果資料被判定為異常，則繪製異常圖表並將之儲存。

                    if np.any(anomalies):
                    # if anomalies.size != 0:
                        
                        # 這是調整異常圖片大小的設定
                        # plt.figure(figsize=(64,34)) 
                        # plt.figure(figsize=(84,54)) 
                        pd.options.display.float_format = '{:,.2f}'.format

                        plt.plot(
                            detect_data.index,
                            detect_data.values,
                            # alpha=0.8,
                            label='Value'
                        )
                        plt.xticks(rotation=25)

                        if algorithm == 'moving_maximum_and_minimum_of_the_historical_data':
                            # 0329 雙層
                            plt.plot(
                                max_df_singma.index,
                                max_df_singma.values,
                                # color="lightsteelblue"
                                color="w"
                            )

                            plt.plot(
                                min_df_singma.index,
                                min_df_singma.values,
                                # color="lightsteelblue"
                                color="w"
                            )

                            # 0329更改繪圖閾值
                            plt.fill_between(detect_data.index, min_np_singma-min_np_stds*threshold, max_np_singma+max_np_stds*threshold, alpha=0.3)
                        else:
                            # 繪製模型計算出來的平均數圖表
                            plt.plot(
                                df_singma.index,
                                df_singma.values,
                                # color="lightsteelblue"
                                color="r"
                            )

                            plt.fill_between(detect_data.index, np_singma-np_stds*threshold, np_singma+np_stds*threshold, alpha=0.3)


                        x = detect_data.iloc[np.where(anomalies>=1)].index
                        y = detect_data.iloc[np.where(anomalies>=1)].Value

                        sns.scatterplot(
                            x=x,
                            y=y,
                            color=sns.color_palette()[3],
                            s=32,
                            label='anomaly'
                        )
                        plt.xticks(rotation=25)
                        plt.legend();
                        # pic_name = 'test%s.png' % ndays
                        pic_name = 'detect.png'
                        plt.savefig(pic_name)

                        try:
                            first_outlier_value_index = detect_data.iloc[np.where(anomalies>=1)[0]].index[0]
                            first_outlier_value = '{0:.0f}'.format(detect_data.iloc[np.where(anomalies>=1)[0][0]].Value)
                        except:
                            first_outlier_value_index = ''
                            first_outlier_value = 'null'
                        
                        try:
                            last_outlier_value_index = detect_data.iloc[np.where(anomalies>=1)[0]].index[-1]
                            last_outlier_value = '{0:.0f}'.format(detect_data.iloc[np.where(anomalies>=1)[0][-1]].Value)
                        except:
                            last_outlier_value_index = ''
                            last_outlier_value = 'null'

                        try:
                            Maximum_outlier_value_index = detect_data.iloc[np.where(anomalies==2)].idxmax().Value
                            Maximum_outlier_value = '{0:.0f}'.format(detect_data.iloc[np.where(anomalies==2)].max().Value)
                        except:
                            Maximum_outlier_value_index = ''
                            Maximum_outlier_value = 'null'

                        try:
                            Minimum_outlier_value_index = detect_data.iloc[np.where(anomalies==1)].idxmin().Value
                            Minimum_outlier_value = '{0:.0f}'.format(detect_data.iloc[np.where(anomalies==1)].min().Value)
                        except:
                            Minimum_outlier_value_index = ''
                            Minimum_outlier_value = 'null'
                        
                        if configArray[dashboard][machine][sub_dashboard]['grafana']['percent_format'] == True:

                            if first_outlier_value != 'null':
                                first_outlier_value = first_outlier_value + "%"
                            
                            if last_outlier_value != 'null':
                                last_outlier_value = last_outlier_value + "%"
                            
                            if Maximum_outlier_value != 'null':
                                Maximum_outlier_value = Maximum_outlier_value + "%"
                            
                            if Minimum_outlier_value != 'null':
                                Minimum_outlier_value = Minimum_outlier_value + "%"

                        anomaly_point_information = '異常首次出現時間︰%s %s \n' % (first_outlier_value_index, first_outlier_value) \
                            +'異常最後出現時間︰%s %s \n' % (last_outlier_value_index, last_outlier_value) \
                            +'異常最大值時間點︰%s %s \n' % (Maximum_outlier_value_index, Maximum_outlier_value) \
                            +'異常最小值時間點︰%s %s \n' % (Minimum_outlier_value_index, Minimum_outlier_value)

                        # 設置機器人資訊
                        TELEGRAM_BOT_TOKEN = '1726742741:AAFdUJfSVQE9fqTV2cCEluumP8NHnUMQ_TI'
                        TELEGRAM_CHAT_ID = '1722334148'
                        PHOTO_PATH_grafana = '/usr/workspace/%s' % pic_name

                        ## 以下是測試區塊
                        string = model_path
                        string = string.split("/")

                        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

                        caption = '\n\n 主機︰%s \n異常指標︰%s \n異常時間︰\n\n%s \n\nURL︰%s' % (string[6], string[7], anomaly_point_information, url)

                        photo_array = [InputMediaPhoto(caption = caption, media=open(PHOTO_PATH_grafana, 'rb')) ]

                        bot.sendMediaGroup(chat_id=TELEGRAM_CHAT_ID, media=photo_array)
                                

                    model.close()
                    plt.clf()


                    


    driver.close()   