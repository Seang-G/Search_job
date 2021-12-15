from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import data_handler
import os

home = os.path.dirname(os.path.realpath(__file__))
languages, sites = data_handler.get_bdata()

def save_chart():
    df = pd.read_csv(f'{home}/static/totals.csv', header=None)
    df.columns = ['# of searched']
    df['site'] = sites * len(languages)
    df['language'] = [languages[i//len(sites)%len(languages)] for i in range(len(df))]
    draw_chart(df)

def draw_chart(df):
    plt.figure(figsize=(8.5, 8))
    palette = sns.color_palette("Blues", as_cmap=True)
    sns.set_theme(style='dark')
    sns.barplot(data=df, x='language', y='# of searched', hue='site')
    plt.tight_layout()
    plt.savefig(f'{home}/static/chart.png')