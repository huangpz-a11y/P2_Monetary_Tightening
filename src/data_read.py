'''
Creates the functions to read the downloaded data for the iShares and S&P indexes.

'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def process_sp_data(data_name,short_name):
    df = pd.read_excel(f'../data/manual/{data_name}.xlsx',skiprows=6)
    df = df.iloc[:-4]
    df.columns = ['date',f'{short_name}']
    df = df.set_index('date')
    df.tail()
    return df

def process_ishares_data(data_name, short_name):
    df = pd.read_csv(f'../data/manual/{data_name}.csv')
    df = df[['Date','Adj Close']]
    df.columns = ['date',f'{short_name}']
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    return df

def combine_dfs(df_ls):
    df = pd.DataFrame(index=df_ls[0].index)
    for i in df_ls:
        df[i.columns[0]] = i
    return df