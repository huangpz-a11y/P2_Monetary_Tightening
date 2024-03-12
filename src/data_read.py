'''
Creates the functions to read the downloaded data for the iShares and S&P indexes.

'''


import pandas as pd
import numpy as np
import warnings
import yfinance as yf
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

import config
DATA_DIR = config.DATA_DIR
BASE_DIR = config.BASE_DIR

def process_sp_data(data_name,short_name):
    """
    Process the S&P data from the manual folder
    """
    path = (BASE_DIR / 'data' / 'manual' / data_name)
    # print(path)
    df = pd.read_excel(f'{path}.xlsx',skiprows=6)
    df = df.iloc[:-4]
    df.columns = ['date',f'{short_name}']
    df = df.set_index('date')
    df.tail()
    return df

def fetch_etfs(etf_ls,start_date,end_date):
    """
    Fetch the ETF data from Yahoo Finance
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame(index=date_range)
    df.index.name = 'date'

    for i in etf_ls:
        shy_data = yf.download(i, start=start_date, end=end_date)
        df[i] = shy_data['Adj Close']
    return df

def combine_dfs(df_ls):
    """
    Combine the ETF dataframes
    """
    df = df_ls[0].copy()
    for i in df_ls[1:]:
        df[i.columns[0]] = i
    df = df.fillna(method='ffill')
    df = df.dropna()
    return df

def save_df(df, data_name):
    """
    Save the dataframe to the pulled folder
    """
    path = (DATA_DIR /'pulled' / data_name)
    df.to_excel(f'{path}.xlsx')

def load_df(data_name,manual=0,csv=False):
    """
    Load the dataframe from the manual or pulled folder
    """
    if manual == 0:
        path = (DATA_DIR /'pulled' / data_name)
    else:
        path = (DATA_DIR /'manual' / data_name)
    
    if csv == True:
        df = pd.read_csv(f'{path}.csv')
    else:
        df = pd.read_excel(f'{path}.xlsx')
    df = df.set_index(df.columns[0])
    return df

def graph_index(df,start_date,end_date, title = 'Treasury by Maturity', filename = ''):
    """
    Graph the index data
    """
    graph_df = df[df.index >= start_date]
    graph_df = graph_df[graph_df.index <= end_date]
    # could also do .last()
    graph_df = graph_df.resample('Q').first()
    
    scaler = 1/graph_df.iloc[0]
    scaled_df = graph_df * scaler
    
    #plt.figure(figsize=(14, 7))
    for col in scaled_df:
        plt.plot(scaled_df.index,scaled_df[col],label=col)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Scaled Price / Ratio Value')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    if filename == '':
        plt.show()
    else:
        plt.savefig(filename)
    plt.close()