import re
import time
import requests
import random
from bs4 import BeautifulSoup as bs

URL = 'https://kr.indeed.com/%EC%B7%A8%EC%97%85'
params = {
    'q': 'go',
    'start': 0,
    'limit': 100
}

# 언어와 페이지를 입력받고 html을 반환하는 함수
def get_html(language, page=0):
    params['q'] = language
    params['start'] = page*100

    response = requests.get(URL, params=params)
    soup = bs(response.text, "html.parser")

    return soup

# 문자열 속 정수를 찾아 정수형태로 반환하는 함수
def get_int_from_str(strin):
    strin = strin.replace(',', '')
    p = re.compile('[0-9]{2,}')
    num = p.findall(strin)[0]

    return int(num)

# 해당 언어에 대한 검색 결과의 총 개수를 반환하는 함수
def get_total(language):
    html = get_html(language)
    total = html.select_one("#searchCountPages").text

    return get_int_from_str(total)

# 하나의 채용 정보를 반환하는 함수
def extract_job(html):
    title = html.select_one("h2.jobTitle > span")['title']
    location = html.select_one(".companyLocation").text
    try: company = html.select_one(".companyName").text
    except: company = ''
    url = 'https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk=' + html['data-jk']

    return [title, location, company, url]

# 해당 언어에 대한 채용 정보를 최대 500개 반환하는 함수
def extract_jobs(language):
    jobs = []
    for page in range(5):
        print(f"Indeed ({language}) : Extracting page {page+1}")
        html = get_html(language, page)
        results = html.select("#mosaic-provider-jobcards > a.tapItem")
        jobs += [extract_job(result) for result in results]
        time.sleep(random.uniform(2, 4))

    return jobs