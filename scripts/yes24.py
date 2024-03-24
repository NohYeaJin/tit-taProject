import time
from datetime import datetime

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re

def check_musical_category(title):
    keywords = ['아동', '가족', '어린이']

    for keyword in keywords:
        if title.find(keyword) != -1:
            return False

    return True

def update_excel(row_num, musical_values, df):
    df.loc[row_num] = musical_values

# 열이 10개인 데이터프레임 생성
data = {'ID': [],
        'TITLE': [],
        'CREATED_AT': [],
        'OPEN_AT': [],
        'LOCATION': [],
        'SOURCE': [],
        'CATEGORY': [],
        'FEAT': [],
        'FILTER_REASON': []}

df = pd.DataFrame(data)

new_filename = datetime.today().strftime("%Y-%m-%d")

driver = webdriver.Chrome()
driver.get('http://ticket.yes24.com/New/Notice/NoticeMain.aspx')

query_txt = '뮤지컬'
element = driver.find_element(By.ID, 'SearchTextbox')
element.send_keys(query_txt)
button = driver.find_element(By.CLASS_NAME, 'notice-srch').find_element(By.TAG_NAME, "a")
button.click()

musical_titles = driver.find_element(By.ID, "BoardList").find_elements(By.TAG_NAME, "tr")

index = 0
start_row = 0
for i in musical_titles:
    # open_dt = i.find_element(By.CLASS_NAME, "open_info")
    # print(open_dt.text)
    musical_value = ["" for _ in range(9)]

    filtered = False
    index += 1
    start_row += 1
    musical_value[0] = index
    musical_value[5] = "ticketlink"
    musical_value[2] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    musical_value[6] = "Musical"

    if not check_musical_category(i.text):
        musical_value[8], musical_value[1] = "musical category invalid(family,Kids)", i.text
        update_excel(start_row, musical_value, df)
        continue

    title = re.findall(r'<(.*?)>', i.text)
    if not title:
        musical_value[8] = "no title!"
        musical_value[1] = i.text
        update_excel(start_row, musical_value, df)
        continue
    musical_value[1] = title[0]

    location = re.findall(r'>\s*-\s*(.*?(?=\s*티켓오픈))\s*', i.text)
    if not location:
        musical_value[8] = "no location!"
        musical_value[1] = i.text
        update_excel(start_row, musical_value, df)
        continue
    musical_value[4] = location[0]
    update_excel(start_row, musical_value, df)

# 시간 지연 이후에 엑셀에 저장
time.sleep(10)  #
df.to_csv(new_filename+'.csv', index=False)