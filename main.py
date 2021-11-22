from flask import Flask, render_template, request
from datetime import datetime
from itertools import product
from pretty_html_table import build_table
import pandas as pd
import data
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', languages=languages, sites=sites)

@app.route('/result')
def result():
    selected_sites = [site for site in sites if request.args.get(site) is not None]
    selected_languages = [language for language in languages if request.args.get(language) is not None]

    sites_n_languages = list(product(selected_sites, selected_languages))
    df_dic = {}
    for site_n_language in sites_n_languages:
        site, language = site_n_language
        df = pd.read_excel(f'{home}\\data\\{now}.xlsx', f'{site}_{language}')
        df_dic[site_n_language] = df

    return render_template('result.html', table=df.to_html())

@app.route('/show')
def show():
    f'''
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://andybrewer.github.io/mvp/mvp.css" rel="stylesheet"></link>
        <title>Show</title>
    </head>
    <body>
        
    </body>
    </html>
    '''

if __name__ == '__main__':
    now = datetime.now().strftime('%Y%m%d')
    home = os.path.dirname(os.path.realpath(__file__))
    if f'{now}.xlsx' in os.listdir(home+'\\data'):
        languages, sites = data.get_bdata()
        app.run()

    else: data.save()