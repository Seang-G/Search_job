from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import data
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', languages=languages, sites=sites)

@app.route('/result')
def result():
    selected_site = request.args.get('site')
    selected_language = request.args.get('language')
    df = pd.read_excel(f'{home}\\data\\{now}.xlsx', f'{selected_site}_{selected_language}')

    return make_table(df[:50].to_html(), selected_language, selected_site)

def make_table(table, language, site):
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
                <h2 align='center'>{language} in {site}</h2>
                <div align='center'>
                    {table}
                </div>
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