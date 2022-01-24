#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import time
import os
# import yaml
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

# with open('api.yml', 'r') as f:
#     apiArray = yaml.load(f)
#     print(apiArray)



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

    driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span').click()
    # driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[15]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span').click()
    modal_box_popping_up = driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/a')
    # modal_box_popping_up = driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[15]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/a')
    ActionChains(driver).move_to_element(modal_box_popping_up).perform()
    driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/ul/li[2]/a').click()
    # driver.find_element(By.XPATH, '/html/body/grafana-app/div/div/div/react-container/div/div[2]/div/div[1]/div/div[2]/div[15]/div/div/div/plugin-component/panel-plugin-graph/grafana-panel/div/div[1]/panel-header/span/span[3]/ul/li[5]/ul/li[2]/a').click()
 
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/export-data-modal/div/div[2]/div[2]/a[1]'))).click()
    except TimeoutException:
        print("ERROR: modal box does not pop up.")
    
    #time.sleep(5) 
    # driver.get_screenshot_as_file("foo.png")

def confirm_whether_there_is_maintenance(datetime, maintenance_list):

    for maintenance_day in maintenance_list:
        if datetime.year == maintenance_day.year and datetime.month == maintenance_day.month and datetime.day == maintenance_day.day:
            maintenance = True
            break
        # elif datetime.day == 2 or datetime.day == 5:
        #     maintenance = True
        #     break
        else:
            maintenance = False
    return maintenance


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

    method = 'DELETE'
    API = '%2Fapi%2Fuser%2F*****'

    maintenance_list = [datetime(2021, 11, 10) ,datetime(2021, 10, 27), datetime(2021, 10, 13),
                        datetime(2021, 9, 29), datetime(2021, 9, 8), datetime(2021, 8, 25),
                        datetime(2021, 8, 11), datetime(2021, 7, 28), datetime(2021, 7, 14),
                        datetime(2021, 6, 30), datetime(2021, 6, 16), datetime(2021, 6, 2),
                        datetime(2021, 5, 19), datetime(2021, 5, 5), datetime(2021, 4, 21),
                        datetime(2021, 4, 7), datetime(2021, 3, 24), datetime(2021, 3, 10),
                        datetime(2021, 2, 24), datetime(2021, 2, 3), datetime(2021, 1, 20),
                        datetime(2021, 1, 6), datetime(2020, 12, 16), datetime(2020, 12, 2),
                        datetime(2020, 11, 18), datetime(2020, 11, 4), datetime(2021, 11, 24),
                        datetime(2021, 12, 8), datetime(2021, 12, 22), datetime(2021, 1, 5)]
    # the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(hours=-8, seconds=-1)
    the_day_before_datetime = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(seconds=-1)


    days = 180
    for i in range(days):
        start_timestemp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000-86400000+1000)
        end_timestamp = str(math.floor(datetime.timestamp(the_day_before_datetime))*1000)
        url = "http://grafana.rd5/d/TnH1dOTMz/monitor-api?orgId=1&fullscreen&panelId=4&var-method=" + method + "&var-api=" + API + "&from=" + start_timestemp + "&to=" + end_timestamp
        # url = 'http://grafana.rd5/d/000000090/ipl-bridge?orgId=1&from=' + start_timestemp + '&to=' + end_timestamp + '&var-db=rd5&var-server=ipl-bridge15.rd5.prod&var-inter=1m&fullscreen&panelId=19'

        print('下載csv檔案')
        download_status = False
        maintenance_day = confirm_whether_there_is_maintenance(the_day_before_datetime, maintenance_list)
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
        file_name = str(i+1) + ".csv"

        os.rename("grafana_data_export.csv", file_name)

        if maintenance_day == True:
            shutil.move(file_name, "/usr/local/airflow/data/maintenance/")
        else:
            shutil.move(file_name, "/usr/local/airflow/data/no_maintenance/")

        the_day_before_datetime = the_day_before_datetime + timedelta(days=-1)

    driver.close()  
