from extractor import saramin, indeed, jobkorea
import pandas as pd
from datetime import datetime
import os
import time

sites = ['Saramin', 'Indeed', 'JobKorea']
languages = ['C', 'C++', 'C#', 'Java', 'JavaScript', 'Python', 'Go']

def save():
    global sites
    global languages

    start_time = time.time()
    home = os.path.dirname(os.path.realpath(__file__))

    # 엑셀 파일 생성
    now = datetime.now().strftime('%Y%m%d')
    writer = pd.ExcelWriter(f'{home}\\data\\{now}.xlsx', mode='w', engine='xlsxwriter')

    total_lst = []
    for language in languages:
        # 검색된 채용 정보의 수 추출
        total_lst.append([saramin.get_total(language),
                        indeed.get_total(language),
                        jobkorea.get_total(language)])

        # 채용 정보 추출
        df_saramin = pd.DataFrame(saramin.extract_jobs(language), columns=['Title', 'Location', 'Company', 'URL'])
        df_indeed = pd.DataFrame(indeed.extract_jobs(language), columns=['Title', 'Location', 'Company', 'URL'])
        df_jobkorea = pd.DataFrame(jobkorea.extract_jobs(language), columns=['Title', 'Location', 'Company', 'URL'])

        # 채용 정보를 엑셀로 저장
        df_saramin.to_excel(writer, sheet_name=f'Saramin_{language}', index=False)
        df_indeed.to_excel(writer, sheet_name=f'Indeed_{language}', index=False)
        df_jobkorea.to_excel(writer, sheet_name=f'JobKorea_{language}', index=False)

    # 채용 정보의 수를 엑셀로 저장
    df_total = pd.DataFrame(total_lst, index=languages, columns=sites)
    df_total.to_excel(writer, sheet_name='Total')

    writer.save()

    total_time = int(time.time() - start_time)
    print(f'걸린 시간 : {total_time//60}분 {total_time%60}초')

def get_bdata():
    global sites
    global languages
    return languages, sites