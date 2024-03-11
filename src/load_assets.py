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
    # df = df[df['RSSD9999'] == date]  
    # df = df.reset_index(drop=True)

    return df 

# load_wrds_reports('ddss0fpozaxonboe')

# #Downloading Data Series from WRDS
# rcfd_data_1 = pd.read_csv(r'../data/manual/ddss0fpozaxonboe.csv') #series 1 of rcfd
# rcfd_data_2 = pd.read_csv(r'../data/manual/dycfrwcdm9puanhs.csv') #series 2 of rcfd
# rcon_data_1 = pd.read_csv(r'../data/manual/m3pzkcjsgvk26dwa.csv') #series 1 of rcon
# rcon_data_2 = pd.read_csv(r'../data/manual/hwv0m9qml6efztsi.csv') #series 2 of rcon
# rcfn_data = pd.read_csv(r'../data/manual/cipzs5x6g2axzlhe.csv') #rcfn