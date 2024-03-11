import pandas as pd
import load_WRDS
import config
import data_read

DATA_DIR = config.DATA_DIR

def load_wrds_reports(file_name):
    path = (DATA_DIR / 'manual' / file_name)
    df = pd.read_csv(f'{path}.csv')
    return df

def clean_assets(df,asset_col,date):
    col_ls = ['RSSD9001','RSSD9017','RSSD9999']
    col_ls.append(asset_col)
    df = df[col_ls]
    df = df.dropna()
    df.columns = ['Bank_ID','bank_name','report_date','gross_asset']
    df = df[df['report_date'] == date]  


    return df 

def clean_loans(df,loan_cols,date):
    col_ls = ['RSSD9001','RSSD9017','RSSD9999']
    col_ls = col_ls + loan_cols
    df = df[col_ls]
    df = df.dropna()
    df.columns = ['Bank_ID','bank_name','report_date','<3m', '3m-1y','1y-3y','3y-5y','5y-15y','>15y']
    df = df[df['report_date'] == date]  

    return df 
