from extractor import saramin, indeed, jobkorea
from datetime import datetime
import pandas as pd
import os
import time

sites = ['Saramin', 'Indeed', 'JobKorea']
languages = ['C', 'C++', 'C#', 'Java', 'JavaScript', 'Python', 'Go']
home = os.path.dirname(os.path.realpath(__file__))
now = datetime.now().strftime('%Y%m%d')

def get_bdata():
    return languages, sites

def save_xlsx():
    start_time = time.time()

    # 엑셀 파일 생성
    writer = pd.ExcelWriter(f'{home}/static/data.xlsx', mode='w', engine='xlsxwriter')

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

def save_totals():
    with open(f'{home}/static/totals.csv', 'w') as f:
        for language in languages:
            f.write(str(saramin.get_total(language))+'\n')
            f.write(str(indeed.get_total(language))+'\n')
            f.write(str(jobkorea.get_total(language))+'\n')
    
def save_version():
    with open(f'{home}/static/version.txt', 'w') as f:
        f.write(now)