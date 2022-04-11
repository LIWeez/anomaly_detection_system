#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import time
import os
import yaml
import sys
import math
from datetime import datetime, timedelta
import turtle
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
    
    #time.sleep(5) 
    # driver.get_screenshot_as_file("foo.png")

def Classifier(datetime, classify_method):
    print("datetime.isoweekday():" + str(datetime.isoweekday()))
    print("classify_method:" +str(classify_method))
    if classify_method == 'check_maintanece':
        print(datetime.isoweekday())
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

    # method = 'DELETE'
    # API = '%2Fapi%2Fuser%2F*****'

    # maintenance_list = [datetime(2021, 11, 10) ,datetime(2021, 10, 27), datetime(2021, 10, 13),
    #                     datetime(2021, 9, 29), datetime(2021, 9, 8), datetime(2021, 8, 25),
    #                     datetime(2021, 8, 11), datetime(2021, 7, 28), datetime(2021, 7, 14),
    #                     datetime(2021, 6, 30), datetime(2021, 6, 16), datetime(2021, 6, 2),
    #                     datetime(2021, 5, 19), datetime(2021, 5, 5), datetime(2021, 4, 21),
    #                     datetime(2021, 4, 7), datetime(2021, 3, 24), datetime(2021, 3, 10),
    #                     datetime(2021, 2, 24), datetime(2021, 2, 3), datetime(2021, 1, 20),
    #                     datetime(2021, 1, 6), datetime(2020, 12, 16), datetime(2020, 12, 2),
    #                     datetime(2020, 11, 18), datetime(2020, 11, 4), datetime(2021, 11, 24),
    #                     datetime(2021, 12, 8), datetime(2021, 12, 22), datetime(2021, 1, 5)]
    # the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(hours=-8, seconds=-1)
    the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=-28, hours=-8, seconds=-1)

    for dashboard in configArray:
        for machine in configArray[dashboard]:
            for sub_dashboard in configArray[dashboard][machine]:
                # for model in configArray[dashboard][machine][sub_dashboard]['model']:
                
                days = sys.argv[1]

                # start_time = sys.argv[1]
                # end_time = sys.argv[2]
                

                for i in range(int(days)):
                    file_path = ''
                    start_timestemp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000-86400000+1000)
                    end_timestamp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000)
                    url = "%s&from=%s&to=%s" % (configArray[dashboard][machine][sub_dashboard]['grafana']['url'], start_timestemp, end_timestamp)
                    
                    print(url)
                    print('下載csv檔案')
                    download_status = False
                    # 這一天的監控資料符合目前指針所指的model要用的資料嗎，如果是的話就返回True。
                    for model_index in range(len(configArray[dashboard][machine][sub_dashboard]['model'])):
                        file_path_status = False
                        file_path_status = Classifier(the_day_before_datetime, configArray[dashboard][machine][sub_dashboard]['model'][model_index]['classify_method'])
                        print("是否驗證成功︰"+str(file_path_status))
                        if file_path_status == True:
                            file_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['data_path']
                            print(file_path)
                            break

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

                    file_name = "%s.csv" % (the_day_before_datetime.strftime('%Y%m%d'))

                    shutil.move("grafana_data_export.csv", "%s/%s" % (file_path, file_name))

                    the_day_before_datetime = the_day_before_datetime + timedelta(days=-1)

                the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=-260, hours=-8, seconds=-1)



    driver.close()  