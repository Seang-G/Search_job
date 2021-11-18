import re
import time
import requests
import random
from bs4 import BeautifulSoup as bs

URL = 'https://www.jobkorea.co.kr/Search/'

# 언어와 페이지를 입력받고 html을 반환하는 함수
def get_html(language, page=1):
    response = requests.get(URL + f'?stext={language}&Page_No={page}')
    soup = bs(response.text, "html.parser")

    return soup

# 문자열 속 정수를 찾아 정수형태로 반환하는 함수
def get_int_from_str(strin):
    strin = strin.replace(',', '')
    p = re.compile('[0-9]+')
    num = p.findall(strin)[0]

    return int(num)

# 해당 언어에 대한 검색 결과의 총 개수를 반환하는 함수
def get_total(language):
    html = get_html(language)
    total = html.select_one("div.list-filter-wrap > p > strong").text

    return get_int_from_str(total)

# 하나의 채용 정보를 반환하는 함수
def extract_job(html):
    title = html.select_one("a.title")['title']
    location = html.select_one(".option > .long").text
    company = html.select_one("a.dev_view")['title']
    url = 'https://www.jobkorea.co.kr/Recruit/GI_Read/' + html['data-gno']

    return [title, location, company, url]

# 해당 언어에 대한 채용 정보를 최대 500개 반환하는 함수
def extract_jobs(language):
    jobs = []
    for page in range(1, 26):
        print(f"JobKorea ({language}) : Extracting page {page}")
        html = get_html(language, page)
        results = html.select(".list-post")[:20]
        jobs += [extract_job(result) for result in results]
        time.sleep(random.uniform(2, 4))

    return jobs