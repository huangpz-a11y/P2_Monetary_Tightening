import data_read
import config
from pathlib import Path
DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)
start_date = config.START_DATE
end_date = config.END_DATE

filename_treasury = OUTPUT_DIR / 'Treasury_by_maturity.png'
filename_mbs = OUTPUT_DIR / 'MBS_and_Treasury.png'

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

sns.set()

# Plot1: Treasury by Maturity
treasury_prices = pd.read_excel("./data/manual/combined_index_df.xlsx")
df_SP_Treasury_bond_index = pd.read_excel("./data/manual/Treasury_Index.xlsx")
df_iShare_MBS_ETF = pd.read_csv("./data/manual/MBS_ETF.csv")

treasury_prices = treasury_prices[['date', 'iShares 0-1', 'iShares 1-3', 'sp 3-5', 'iShares 7-10', 'iShares 10-20', 'iShares 20+']].set_index('date')
data_read.graph_index(treasury_prices, start_date, end_date, filename = filename_treasury)



# Plot2: MBS ETF vs SP Treasury Bond Index
df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.set_index('date')
df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.loc[(df_SP_Treasury_bond_index.index >= start_date) & (df_SP_Treasury_bond_index.index <= end_date)].resample('Q').first()

df_iShare_MBS_ETF = df_iShare_MBS_ETF[['Adj Close', 'Date']].rename(columns={'Adj Close':'iShares MBS ETF', 'Date':'date'}).set_index('date')
df_iShare_MBS_ETF.index = pd.to_datetime(df_iShare_MBS_ETF.index)
df_iShare_MBS_ETF = df_iShare_MBS_ETF.loc[(df_iShare_MBS_ETF.index >= start_date) & (df_iShare_MBS_ETF.index <= end_date)].resample('Q').first()

joined_df = pd.concat([df_SP_Treasury_bond_index, df_iShare_MBS_ETF], axis=1)
data_read.graph_index(joined_df, start_date, end_date, title = 'MBS ETF vs SP Treasury Bond Index', filename = filename_mbs)
