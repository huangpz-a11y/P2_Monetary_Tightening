import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

#Downloading Data Series from WRDS
rcfd_data_1 = pd.read_csv(r'../data/manual/ddss0fpozaxonboe.csv') #series 1 of rcfd
rcfd_data_2 = pd.read_csv(r'../data/manual/dycfrwcdm9puanhs.csv') #series 2 of rcfd
rcon_data_1 = pd.read_csv(r'../data/manual/m3pzkcjsgvk26dwa.csv') #series 1 of rcon
rcon_data_2 = pd.read_csv(r'../data/manual/hwv0m9qml6efztsi.csv') #series 2 of rcon
rcfn_data = pd.read_csv(r'../data/manual/cipzs5x6g2axzlhe.csv') #rcfn

#domestic and foreign branchs
asset_level_0 = rcfd_data_2[['RSSD9001','RSSD9017','RSSD9999','RCFD2170']]
asset_level_0 = asset_level_0.fillna(0)
filtered_asset_level_0 = asset_level_0[asset_level_0['RSSD9999'] == '03/31/2022']

#domestic
asset_level = rcon_data_2[['RSSD9001','RSSD9017','RSSD9999','RCON2170']]
asset_level = asset_level.fillna(0)
filtered_asset_level = asset_level[asset_level['RSSD9999'] == '03/31/2022']

GSIB = [852218, 480228, 476810, 413208, #JP Morgan, Bank of America, Citigroup, HSBC
       2980209, 2182786, 541101, 655839, 1015560, 229913,#Barclays, Goldman Sachs, BNY Mellon, CCB COMMUNITY BANK, ICBC, Mizuho
       1456501, 722777, 35301, 925411, 497404, 3212149, #Morgan Stanley, Santander, State Street, Sumitomo Mitsui, TD Bank, UBS
       451965] #wells fargo

total_assets_all = pd.concat([filtered_asset_level,filtered_asset_level_0])

total_assets_all = total_assets_all.sort_index()

total_assets_GSIB = total_assets_all[total_assets_all['RSSD9001'].isin(GSIB)]

total_assets_large_ex_GSIB = total_assets_all[(~total_assets_all['RSSD9001'].isin(GSIB)) & (total_assets_all['RCFD2170'] > 1384000)]
bank_id_large_ex_GSIB = []
for bank_id in total_assets_large_ex_GSIB['RSSD9001']:
       bank_id_large_ex_GSIB.append(bank_id)

total_assets_small = total_assets_all[(~total_assets_all['RSSD9001'].isin(GSIB)) & (total_assets_all['RCFD2170'] <= 1384000)]
bank_id_small = []
for bank_id in total_assets_small['RSSD9001']:
       bank_id_small.append(bank_id)

##FIRST LIEN LOANS
df_loans_first_lien_domestic = rcon_data_1[['RSSD9001','RSSD9017', 'RSSD9999', 'RCONA564', 'RCONA565', 'RCONA566', 'RCONA567', 'RCONA568', 'RCONA569']]
df_loans_first_lien_domestic = df_loans_first_lien_domestic.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCONA564': '<3m',
    'RCONA565': '3m-1y',
    'RCONA566': '1y-3y',
    'RCONA567': '3y-5y',
    'RCONA568': '5y-15y',
    'RCONA569': '>15y'
})
df_loans_first_lien_domestic = df_loans_first_lien_domestic[df_loans_first_lien_domestic['report_date'] == '03/31/2022']

first_lien_all = df_loans_first_lien_domestic

first_lien_GSIB = df_loans_first_lien_domestic[df_loans_first_lien_domestic['RSSD9001'].isin(GSIB)]

first_lien_large_ex_GSIB = df_loans_first_lien_domestic[(~df_loans_first_lien_domestic['RSSD9001'].isin(GSIB)) & (df_loans_first_lien_domestic['RSSD9001'].isin(bank_id_large_ex_GSIB))]

first_lien_small = df_loans_first_lien_domestic[(~df_loans_first_lien_domestic['RSSD9001'].isin(GSIB)) & (df_loans_first_lien_domestic['RSSD9001'].isin(bank_id_small))]

##LOANS AND LEASES (NOT SECURED BY FIRST LIEN)

df_loans_exc_first_lien = rcfd_data_1[['RSSD9001','RSSD9017', 'RSSD9999', 'RCFDA570', 'RCFDA571', 'RCFDA572', 'RCFDA573', 'RCFDA574', 'RCFDA575']]
df_loans_exc_first_lien = df_loans_exc_first_lien.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCFDA570': '<3m',
    'RCFDA571': '3m-1y',
    'RCFDA572': '1y-3y',
    'RCFDA573': '3y-5y',
    'RCFDA574': '5y-15y',
    'RCFDA575': '>15y'
})
df_loans_exc_first_lien = df_loans_exc_first_lien.dropna()
df_loans_exc_first_lien = df_loans_exc_first_lien[df_loans_exc_first_lien['report_date'] == '03/31/2022']

df_loans_exc_first_lien_domestic = rcon_data_2[['RSSD9001','RSSD9017', 'RSSD9999', 'RCONA570', 'RCONA571', 'RCONA572', 'RCONA573', 'RCONA574', 'RCONA575']]
df_loans_exc_first_lien_domestic = df_loans_exc_first_lien_domestic.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCONA570': '<3m',
    'RCONA571': '3m-1y',
    'RCONA572': '1y-3y',
    'RCONA573': '3y-5y',
    'RCONA574': '5y-15y',
    'RCONA575': '>15y'
})
df_loans_exc_first_lien_domestic = df_loans_exc_first_lien_domestic.dropna()
df_loans_exc_first_lien_domestic = df_loans_exc_first_lien_domestic[df_loans_exc_first_lien_domestic['report_date'] == '03/31/2022']

df_other_loan = pd.concat([df_loans_exc_first_lien_domestic, df_loans_exc_first_lien])
df_other_loan = df_other_loan.sort_index()

other_loan_all = df_other_loan

other_loan_GSIB = other_loan_all[other_loan_all['RSSD9001'].isin(GSIB)]

other_loan_large_ex_GSIB = other_loan_all[(~other_loan_all['RSSD9001'].isin(GSIB)) & (other_loan_all['RSSD9001'].isin(bank_id_large_ex_GSIB))]

other_loan_small= other_loan_all[(~other_loan_all['RSSD9001'].isin(GSIB)) & (other_loan_all['RSSD9001'].isin(bank_id_small))]


##RMBS

df_RMBS = rcfd_data_1[['RSSD9001','RSSD9017', 'RSSD9999', 'RCFDA555', 'RCFDA556', 'RCFDA557', 'RCFDA558', 'RCFDA559', 'RCFDA560']]
df_RMBS = df_RMBS.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCFDA555': '<3m',
    'RCFDA556': '3m-1y',
    'RCFDA557': '1y-3y',
    'RCFDA558': '3y-5y',
    'RCFDA559': '5y-15y',
    'RCFDA560': '>15y'
})
df_RMBS = df_RMBS.dropna()
df_RMBS = df_RMBS[df_RMBS['report_date'] == '03/31/2022']

#Form 051 - Domestic
df_RMBS_dom = rcon_data_1[['RSSD9001','RSSD9017', 'RSSD9999', 'RCONA555', 'RCONA556', 'RCONA557', 'RCONA558', 'RCONA559', 'RCONA560']]
df_RMBS_dom = df_RMBS_dom.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCONA555': '<3m',
    'RCONA556': '3m-1y',
    'RCONA557': '1y-3y',
    'RCONA558': '3y-5y',
    'RCONA559': '5y-15y',
    'RCONA560': '>15y'
})
df_RMBS_dom = df_RMBS_dom.dropna()
df_RMBS_dom = df_RMBS_dom[df_RMBS_dom['report_date'] == '03/31/2022']

df_RMBS_Final = pd.concat([df_RMBS_dom, df_RMBS])
df_RMBS_Final = df_RMBS_Final.sort_index()

RMBS_all = df_RMBS_Final

RMBS_GSIB = RMBS_all[RMBS_all['RSSD9001'].isin(GSIB)]

RMBS_large_ex_GSIB = RMBS_all[~(RMBS_all['RSSD9001'].isin(GSIB)) & (RMBS_all['RSSD9001'].isin(bank_id_large_ex_GSIB))]

RMBS_small = RMBS_all[~(RMBS_all['RSSD9001'].isin(GSIB)) & (RMBS_all['RSSD9001'].isin(bank_id_small))]


##Treasury and Other (non-RMBs)

df_non_RMBS = rcfd_data_2[['[RSSD9001','RSSD9017', 'RSSD9999', 'RCFDA549', 'RCFDA550', 'RCFDA551', 'RCFDA552', 'RCFDA553', 'RCFDA554']]
df_non_RMBS = df_non_RMBS.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCFDA549': '<3m',
    'RCFDA550': '3m-1y',
    'RCFDA551': '1y-3y',
    'RCFDA552': '3y-5y',
    'RCFDA553': '5y-15y',
    'RCFDA554': '>15y'
})
df_non_RMBS = df_non_RMBS.dropna()
df_non_RMBS = df_non_RMBS[df_non_RMBS['report_date'] == '03/31/2022']

#Form 051 - Domestic
df_non_RMBS_dom = rcon_data_2[['RSSD9001','RSSD9017','RSSD9999', 'RCONA549', 'RCONA550', 'RCONA551', 'RCONA552', 'RCONA553', 'RCONA554']]
df_non_RMBS_dom = df_non_RMBS_dom.rename(columns={
    'RSSD9001': 'bank_id',
    'RSSD9017': 'bank_name',
    'RSSD9999': 'report_date',
    'RCONA549': '<3m',
    'RCONA550': '3m-1y',
    'RCONA551': '1y-3y',
    'RCONA552': '3y-5y',
    'RCONA553': '5y-15y',
    'RCONA554': '>15y'
})
df_non_RMBS_dom = df_non_RMBS_dom.dropna()
df_non_RMBS_dom = df_non_RMBS_dom[df_non_RMBS_dom['report_date'] == '03/31/2022']

df_treasury_and_others = pd.concat([df_non_RMBS_dom, df_non_RMBS])
df_treasury_and_others = df_treasury_and_others.sort_index()

treasury_and_others_all = df_treasury_and_others

treasury_and_other_GSIB = treasury_and_others_all[treasury_and_others_all['RSSD9001'].isin(GSIB)]

treasury_and_other_large_ex_GSIB = treasury_and_others_all[~(treasury_and_others_all['RSSD9001'].isin(GSIB)) & (treasury_and_others_all['RSSD9001'].isin(bank_id_large_ex_GSIB)) ]

treasury_and_other_small = RMBS_all[~(RMBS_all['RSSD9001'].isin(GSIB)) & (RMBS_all['RSSD9001'].isin(bank_id_small))]

##Breakdown by Bank Size and Asset Class (total assets, first lien loans, RMBs, treasury and other, and other loans)

total_assets_all # total assets all banks
total_assets_GSIB # total assets GSIB banks
total_assets_large_ex_GSIB # total assets for large banks excl. GSIB
total_assets_small # total assets small banks

first_lien_all # total first lien loans for all banks
first_lien_GSIB # total first lien loans for all GSIB banks
first_lien_large_ex_GSIB # total first lien loans for large banks excl. GSIB
first_lien_small #total first lien loans for small banks

other_loan_all # total other loans all banaks
other_loan_GSIB # total other loans GSIB banks
other_loan_large_ex_GSIB # total other loans large banks excl. GSIB
other_loan_small # total other loans small banks

RMBS_all # total RMBS for all banks
RMBS_GSIB # total RMBS for all GSIB banks
RMBS_large_ex_GSIB # total RMBS for all large banks excl. GSIB
RMBS_small # total RMBS for small banks

treasury_and_others_all # total treasury and other all banks
treasury_and_other_GSIB # total treasury and other all GSIB banks
treasury_and_other_large_ex_GSIB # total treasury and other for large banks excl. GSIB
treasury_and_other_small # total treasury and other for small banks

















