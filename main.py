from flask import Flask, render_template, request, Response, send_file
from io import StringIO
import pandas as pd
import data_handler
import chart
import re
import os

app = Flask(__name__)

home = os.path.dirname(os.path.realpath(__file__))
sites = ['Saramin', 'Indeed', 'JobKorea']
languages = ['C', 'C++', 'C#', 'Java', 'JavaScript', 'Python', 'Go']

@app.route('/')
def index():
    with open(f"{home}/static/version.txt", 'r') as f:
        version = f.read()
    return render_template('index.html', languages=languages, sites=sites, version=version)

@app.route('/result')
def result():
    selected_site = request.args.get('site')
    selected_language = request.args.get('language')
    df = pd.read_excel(f'{home}/static/data.xlsx', f'{selected_site}_{selected_language}')
    
    return make_table(df[:100].to_html(), selected_language, selected_site)

@app.route('/download')
def download():
    return send_file(f'{home}/static/data.xlsx',
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    attachment_filename='일자리 데이터.xlsx')

def make_table(table, language, site):
    p = re.compile(r"https://[0-9a-zA-Z./_?=%]*")
    for url in p.findall(table):
        table = table.replace(url, f"<a href='{url}'>{url}</a>")
    return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <link href="https://andybrewer.github.io/mvp/mvp.css" rel="stylesheet"></link>
            </head>
            <body>
                    <header>
                        <a href="/">
                            <h3>Back to main</h3>
                        </a>
                    </header>
                <h2 align='center'>{site} in {language}</h2>
                <div align='center'>
                    {table}
                </div>
            </body>
            </html>
            '''

def save_all():
    data_handler.save_xlsx()
    data_handler.save_version()
    data_handler.save_totals()
    chart.save_chart()

if __name__ == '__main__':
    update = False
    if update: save_all()
    else: app.run()