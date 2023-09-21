from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import wget
import os
from icecream import ic
from webdriver_manager.chrome import ChromeDriverManager

chrome_option = webdriver.ChromeOptions()

# chrome_option.add_argument('headless')                  # Hide Web-browser
chrome_option.add_argument('window-size=1920x1080')
chrome_option.add_argument('disable-gpu')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_option)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
#                           options=chrome_option)

# 네이버 이동
driver.get('https://www.naver.com')

# 검색창 찾기
input_search = driver.find_element(By.ID, 'query')
# input_search = driver.find_element(By.NAME, 'query')
# input_search = driver.find_element(By.CLASS_NAME, 'search_input')
# input_search = driver.find_element(By.CSS_SELECTOR, '#query')           # '#' : Element ID
# input_search = driver.find_element(By.CSS_SELECTOR, '.search_input')    # '.' : Element Class Name
time.sleep(1)

# 검색어 입력
input_search.send_keys('네이버 영화')
time.sleep(1)

# 엔터키 입력
input_search.send_keys(Keys.ENTER)
time.sleep(1)

# 영화카드를 담고있는 박스
card_area = driver.find_element(By.CSS_SELECTOR, '.card_area._panel') # class="card_area _panel"

total_page = driver.find_element(By.CSS_SELECTOR, '._total')
total_page = int(total_page.text)
next_link = driver.find_element(By.CSS_SELECTOR, '.pg_next.on._next')

for _ in range(total_page):
    time.sleep(1)
    movie_list = card_area.find_elements(By.CSS_SELECTOR, '.card_item')

    for movie in movie_list:
        try:
            ic('=======================================================================')
            # 영화 상세페이지
            link = movie.find_element(By.CSS_SELECTOR, '.img_box')
            link = link.get_attribute('href')

            # 영화 고유코드
            code = link.split('&os=')[1][:8]

            # 영화포스터
            img = movie.find_element(By.TAG_NAME, 'img')
            img_url = img.get_attribute('src')

            # Image 폴더존재여부 확인
            if os.path.exists('./images') is False:
                os.mkdir('images')

            # 포스터 이미지 다운로드
            wget.download(img_url, f'./images/{code}.jpg')

            # 큰 포스터 이미지 다운로드
            origin_url = img_url.replace('174x246', '600x800')
            wget.download(origin_url, f'./images/{code}_origin.jpg')

            # 영화제목
            title = movie.find_element(By.CSS_SELECTOR, '.area_text_box')
            title = title.text

            info_list = movie.find_elements(By.CSS_SELECTOR, '.info_group')

            # 영화 장르, 상영시간
            _, category, running_time = info_list[0].text.split('\n')  # 개요\n스릴러\n180분

            # 개봉일, 평점
            _, open_date, _, score = info_list[1].text.split('\n')

            # 출연배우
            if len(info_list[2].text) != 0:
                _, actors = info_list[2].text.split('\n')
            else:
                actors = ''

            ic(title)
            ic(category)
            ic(running_time)
            ic(open_date)
            ic(score)
            ic(actors)
            ic(link)
            ic(img_url)
        except Exception as e:
            ic(e)

    next_link.click()

driver.close()

































