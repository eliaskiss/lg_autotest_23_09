from selenium import webdriver
from bs4 import BeautifulSoup as bs
import wget
import os
from icecream import ic

chrome_option = webdriver.ChromeOptions()
# chrome_option.add_argument('headless')
chrome_option.add_argument('window-size=1920x1080')
chrome_option.add_argument('disable-gpu')
driver = webdriver.Chrome('chromedriver.exe', options=chrome_option)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_option)

# Wait for web-browser loading
driver.implicitly_wait(3)

# 네이버로 이동
driver.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EC%98%81%ED%99%94&oquery=%EB%84%A4%EC%9D%B4%EB%B2%84+%EC%98%81%ED%99%94&tqi=iMO73lp0J14ssdaumLVssssstiw-342447')

# 해당 페이지를 html파일로 저장
with open('naver.html', 'w', encoding='utf8') as f:
    f.write(driver.page_source)

soup = bs(driver.page_source, 'html.parser')
# soup = bs(driver.page_source, 'lxml') # pip install lxml
# soup = bs(driver.page_source, 'lxml-xml') # Only XML
# soup = bs(driver.page_source, 'xml') # Only XML
# soup = bs(driver.page_source, 'html5lib')
driver.close()

# 네이버 영화링크
current_move_link = soup.select_one('.card_area._panel')
movie_list = current_move_link.select('.card_item')

for movie in movie_list:
    try:
        ic('===========================================================================')
        # 영화 상세페이지
        link = movie.select_one('.img_box')
        link = link['href']

        # 영화 고유코드
        code = link.split('&os=')[1][:8]

        # 영화포스터
        img = movie.select_one('img')
        img_url = img['src']

        # Image 폴더존재여부 확인
        if os.path.exists('./images') is False:
            os.mkdir('images')

        # 포스터 이미지 다운로드
        wget.download(img_url, f'./images/{code}.jpg')

        # 큰 포스터 이미지 다운로드
        origin_url = img_url.replace('174x246', '600x800')
        wget.download(origin_url, f'./images/{code}_origin.jpg')

        # 영화제목
        title = movie.select_one('.area_text_box')
        title = title.text

        info_list = movie.select('.info_group')

        # 영화장르, 상영시간
        _, category, running_time = info_list[0].text.strip().split(' ')

        # 개봉일, 평점
        _, open_date, _, score = info_list[1].text.strip().split(' ')

        # 출연배우
        if len(info_list[2].text) != 0:
            actors = info_list[2].text
            actors = actors.replace('출연', '')
            actors = actors.strip()
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

print('Crawling is done!!!')