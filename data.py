import pandas as pd
import saramin
import os

os.chdir("파이썬 응용/텀 프로젝트/Search_job")

print(saramin.get_total('python'))
df = pd.DataFrame(saramin.extract_jobs('python'), columns=['Title', 'Location', 'Company', 'Career', 'URL'])
df.to_excel('saramin.xlsx')