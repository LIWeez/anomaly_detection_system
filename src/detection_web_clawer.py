#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import time
import os
import yaml
import sys
import math
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

with open('/usr/workspace/config/prod.yml', 'r') as f:
    configArray = yaml.safe_load(f)

def login(drive,username,passwd):
    input = driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/div/div/div[2]/div[1]/form/div[1]/input')
    input.send_keys(username)
    print('grafana輸入帳號中⋯')
    input = driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/div/div/div[2]/div[1]/form/div[2]/input')
    input.send_keys(passwd)
    print('grafana輸入密碼中⋯')

    input.send_keys(Keys.ENTER)
    print('登入完成')
    drive.implicitly_wait(3000)
    driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/div/div/div[2]/div[1]/form/div[3]/button').click()
    # skip changing password  
    driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/div/div/div[2]/div[2]/form/div[3]/a').click()

def download_csv_file(url):    
    driver.get(url)
    driver.find_element(By.XPATH, "/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[%s]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span" % (configArray[dashboard][machine][sub_dashboard]['grafana']['div_id'])).click()
    # driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[15]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span').click()
    modal_box_popping_up = driver.find_element(By.XPATH, "/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[%s]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/a" % (configArray[dashboard][machine][sub_dashboard]['grafana']['div_id']))
    # modal_box_popping_up = driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[15]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/a')
    ActionChains(driver).move_to_element(modal_box_popping_up).perform()
    driver.find_element(By.XPATH, "/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[%s]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/ul/li[2]/a" % (configArray[dashboard][machine][sub_dashboard]['grafana']['div_id'])).click()
    # driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[15]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/ul/li[2]/a').click()
 
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/export-data-modal/div/div[2]/div[2]/a[1]'))).click()
    except TimeoutException:
        print("ERROR: modal box does not pop up.")
    
    #time.sleep(5) 
    # driver.get_screenshot_as_file("foo.png")

def Classifier(datetime, classify_method):
    print(datetime.isoweekday())
    print(classify_method)
    file_path_status = False
    if classify_method == 'check_maintanece':
        if datetime.isoweekday() != 3:
            return file_path_status

        week_number = datetime.isocalendar()[1]
        # 因維護遇到節日時會延遲到下一週，因此需要更改週次的數值以維持準確性。
        if datetime.isocalendar()[1] >= 8:
            week_number += 1
        if datetime.isocalendar()[1] >= 38:
            week_number += 1

        if week_number % 2 == 1 :
            file_path_status = True
            return file_path_status

    elif classify_method == 'update_days':
        if datetime.isoweekday() == 2 or datetime.isoweekday() == 5:
            file_path_status = True
            return file_path_status
    else:
        return file_path_status


if __name__ == '__main__':
    username="admin"  
    passwd="admin" 
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    
    print('進入grafana網頁')
    driver.get("http://grafana.rd5/")
    login(driver, username, passwd)  

    the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(seconds=-1)

    for dashboard in configArray:
        for machine in configArray[dashboard]:
            for sub_dashboard in configArray[dashboard][machine]:

                file_path = ''
                start_timestemp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000-86400000+1000)
                end_timestamp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000)
                url = "%s&from=%s&to=%s" % (configArray[dashboard][machine][sub_dashboard]['grafana']['url'], start_timestemp, end_timestamp)
                print(url)
                print('下載csv檔案')
                download_status = False
                for model_index in range(len(configArray[dashboard][machine][sub_dashboard]['model'])):
                    file_path_status = False
                    file_path_status = Classifier(the_day_before_datetime, configArray[dashboard][machine][sub_dashboard]['model'][model_index]['classify_method'])
                    if file_path_status == True:
                        file_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['data_path']
                        print(file_path)
                        break
                    if configArray[dashboard][machine][sub_dashboard]['model'][model_index]['classify_method'] == 'normal':
                        file_path = configArray[dashboard][machine][sub_dashboard]['model'][model_index]['data_path']
                        print(file_path)
                        break
                while download_status == False:
                    size = 0
                    download_csv_file(url)
                    time.sleep(40/1000)
                    try:
                        size = os.path.getsize('grafana_data_export.csv')
                    except Exception as e:
                        print('download error.')
                    if size > 100:
                        download_status = True

                file_name = "%s.csv" % (the_day_before_datetime.strftime('%Y%m%d'))

                shutil.move("grafana_data_export.csv", "%s/%s" % (file_path, file_name))

                the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(seconds=-1)

    driver.close()   