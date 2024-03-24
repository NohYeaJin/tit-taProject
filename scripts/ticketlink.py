import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import re

from musical.models import Musicals


def check_musical_category(title):
    keywords = ['아동', '가족', '어린이']

    for keyword in keywords:
        if title.find(keyword) != -1:
            return False

    return True

def update_excel(row_num, musical_values, df):
    df.loc[row_num] = musical_values

def convert_str_to_dt(open_date_str):
    # 괄호와 괄호 안의 문자열을 삭제하는 정규식 패턴
    pattern = re.compile(r'\(.*?\)')

    # 정규식을 사용하여 문자열에서 괄호와 괄호 안의 문자열을 삭제
    date_str = re.sub(pattern, '', open_date_str)

    # 문자열을 datetime 객체로 변환
    return datetime.strptime(date_str, '%Y.%m.%d %H:%M')


def run():
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

    # new_filename = datetime.today().strftime("%Y-%m-%d")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")  # 창을 띄우지 않음
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 보안 비활성화
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    driver.get('https://www.ticketlink.co.kr/help/notice')

    query_txt = '뮤지컬'
    element = driver.find_element(By.NAME, 'title')
    element.send_keys(query_txt)
    button = driver.find_element(By.NAME, 'searchBtn')
    button.click()

    musical_titles = driver.find_element(By.ID, "nTableBody").find_elements(By.TAG_NAME, "tr")

    index = 0
    start_row = 0

    for i in musical_titles:
        musical_value = ["" for _ in range(9)]

        filtered = False
        index += 1
        start_row += 1
        musical_value[0] = index
        musical_value[5] = "ticketlink"
        musical_value[2] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        musical_value[6] = "Musical"

        raw_title = i.find_element(By.TAG_NAME, "a")
        open_date = convert_str_to_dt(i.find_element(By.CLASS_NAME, 'open_info').text.replace('오픈: ', ''))

        if not check_musical_category(raw_title.text):
            musical_value[8], musical_value[1] = "musical category invalid(family,Kids)", raw_title.text
            update_excel(start_row, musical_value, df)
            Musicals(title=raw_title.text, ticket_time=open_date, location='', source="ticketlink", fail=True,
                     fail_reason=musical_value[8]).save()
            continue

        title = re.findall(r'<(.*?)>', raw_title.text)
        if not title:
            musical_value[8] = "no title!"
            musical_value[1] = raw_title.text
            update_excel(start_row, musical_value, df)
            Musicals(title=raw_title.text, ticket_time=open_date, location='', source="ticketlink", fail=True,
                     fail_reason=musical_value[8]).save()
            continue
        musical_value[1] = title[0]

        location = re.findall(r'>\s*-\s*(.*?(?=\s*티켓오픈))\s*', raw_title.text)
        if not location:
            musical_value[8] = "no location!"
            musical_value[1] = raw_title.text
            update_excel(start_row, musical_value, df)
            Musicals(title=title[0], ticket_time=open_date, location='', source="ticketlink", fail=True,
                     fail_reason=musical_value[8]).save()
            continue
        musical_value[4] = location[0]

        # already crawled or exists
        if Musicals.objects.filter(title__iexact=title[0], location__iexact=location[0]).exists():
            continue

        Musicals(title=title[0], ticket_time=open_date, location=location[0], source="ticketlink").save()
    #     update_excel(start_row, musical_value, df)
    #
    # # 시간 지연 이후에 엑셀에 저장
    # time.sleep(10)  #
    # df.to_csv(new_filename+'.csv', index=False)