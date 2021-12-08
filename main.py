from flask import Flask, render_template, request
from datetime import datetime
from itertools import product
import pandas as pd
import data
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', languages=languages, sites=sites)

@app.route('/result')
def result():
    # selected_sites = [site for site in sites if request.args.get(site) is not None]
    # selected_languages = [language for language in languages if request.args.get(language) is not None]

    # sites_n_languages = list(product(selected_sites, selected_languages))
    # df_dic = {}
    # for site_n_language in sites_n_languages:
    #     site, language = site_n_language
    #     df = pd.read_excel(f'{home}\\data\\{now}.xlsx', f'{site}_{language}')
    #     df_dic[site_n_language] = df
    selected_site = request.args.get('site')
    selected_language = request.args.get('language')
    df = pd.read_excel(f'{home}\\data\\{now}.xlsx', f'{selected_site}_{selected_language}')

    return render_template('result.html', site=selected_site, language=selected_language)

@app.route('/Saramin_C')
def show():
    df = pd.read_excel(f'{home}\\data\\{now}.xlsx', 'Saramin_C')
    return make_table_good(df[:10].to_html())

def make_table_good(table):
    return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <link href="https://andybrewer.github.io/mvp/mvp.css" rel="stylesheet"></link>
            </head>
            <body>
                {table}
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