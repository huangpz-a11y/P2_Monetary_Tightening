import pandas as pd
import load_WRDS
import config

DATA_DIR = config.DATA_DIR
OUTPUT_DIR = config.OUTPUT_DIR

def get_RMBs(rcfd_series_1, rcon_series_1, report_date = '03/31/2022'):
    
    #domestic and foreign
    df_RMBS = rcfd_series_1[['rssd9001', 'rssd9017', 'rssd9999', 'rcfda555', 'rcfda556', 'rcfda557', 'rcfda558', 'rcfda559', 'rcfda560']]
    df_RMBS = df_RMBS.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcfda555': '<3m',
        'rcfda556': '3m-1y',
        'rcfda557': '1y-3y',
        'rcfda558': '3y-5y',
        'rcfda559': '5y-15y',
        'rcfda560': '>15y'
    })
    df_RMBS = df_RMBS.dropna()
    df_RMBS = df_RMBS[df_RMBS['report_date'] == report_date]

    #domestic only
    df_RMBS_dom = rcon_series_1[['rssd9001','rssd9017', 'rssd9999', 'rcona555', 'rcona556', 'rcona557', 'rcona558', 'rcona559', 'rcona560']]
    df_RMBS_dom = df_RMBS_dom.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcona555': '<3m',
        'rcona556': '3m-1y',
        'rcona557': '1y-3y',
        'rcona558': '3y-5y',
        'rcona559': '5y-15y',
        'rcona560': '>15y'
    })
    df_RMBS_dom = df_RMBS_dom.dropna()
    df_RMBS_dom = df_RMBS_dom[df_RMBS_dom['report_date'] == report_date]
    
    df_RMBS_Final = pd.concat([df_RMBS_dom, df_RMBS])
    df_RMBS_Final = df_RMBS_Final.sort_index()
    
    return df_RMBS_Final


def get_treasuries(rcfd_series_2, rcon_series_2, report_date = '03/31/2022'):

    #domestic and foreign
    df_non_RMBS = rcfd_series_2[['rssd9001','rssd9017', 'rssd9999', 'rcfda549', 'rcfda550', 'rcfda551', 'rcfda552', 'rcfda553', 'rcfda554']]
    df_non_RMBS = df_non_RMBS.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcfda549': '<3m',
        'rcfda550': '3m-1y',
        'rcfda551': '1y-3y',
        'rcfda552': '3y-5y',
        'rcfda553': '5y-15y',
        'rcfda554': '>15y'
    })
    df_non_RMBS = df_non_RMBS.dropna()
    df_non_RMBS = df_non_RMBS[df_non_RMBS['report_date'] == report_date]

    #domestic only
    df_non_RMBS_dom = rcon_series_2[['rssd9001','rssd9017','rssd9999', 'rcona549', 'rcona550', 'rcona551', 'rcona552', 'rcona553', 'rcona554']]
    df_non_RMBS_dom = df_non_RMBS_dom.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcona549': '<3m',
        'rcona550': '3m-1y',
        'rcona551': '1y-3y',
        'rcona552': '3y-5y',
        'rcona553': '5y-15y',
        'rcona554': '>15y'
    })
    df_non_RMBS_dom = df_non_RMBS_dom.dropna()
    df_non_RMBS_dom = df_non_RMBS_dom[df_non_RMBS_dom['report_date'] == report_date]
    df_non_RMBS_dom

    df_treasury_and_others = pd.concat([df_non_RMBS_dom, df_non_RMBS])
    df_treasury_and_others = df_treasury_and_others.sort_index()
    
    return df_treasury_and_others


def get_loans(rcon_series_1, report_date = '03/31/2022'):

    df_loans_first_lien_domestic = rcon_series_1[['rssd9001','rssd9017', 'rssd9999', 'rcona564', 'rcona565', 'rcona566', 'rcona567', 'rcona568', 'rcona569']]
    df_loans_first_lien_domestic = df_loans_first_lien_domestic.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcona564': '<3m',
        'rcona565': '3m-1y',
        'rcona566': '1y-3y',
        'rcona567': '3y-5y',
        'rcona568': '5y-15y',
        'rcona569': '>15y'
    })
    df_loans_first_lien_domestic = df_loans_first_lien_domestic[df_loans_first_lien_domestic['report_date'] == report_date]
    return df_loans_first_lien_domestic


def get_other_loan(rcon_series_2, rcfd_series_1, report_date = '03/31/2022'):

    #domestic and foreign
    df_loans_exc_first_lien = rcfd_series_1[['rssd9001','rssd9017', 'rssd9999', 'rcfda570', 'rcfda571', 'rcfda572', 'rcfda573', 'rcfda574', 'rcfda575']]
    df_loans_exc_first_lien = df_loans_exc_first_lien.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcfda570': '<3m',
        'rcfda571': '3m-1y',
        'rcfda572': '1y-3y',
        'rcfda573': '3y-5y',
        'rcfda574': '5y-15y',
        'rcfda575': '>15y'
    })
    df_loans_exc_first_lien = df_loans_exc_first_lien.dropna()
    df_loans_exc_first_lien = df_loans_exc_first_lien[df_loans_exc_first_lien['report_date'] ==  report_date]

    df_loans_exc_first_lien_domestic = rcon_series_2[['rssd9001', 'rssd9017', 'rssd9999', 'rcona570', 'rcona571', 'rcona572', 'rcona573', 'rcona574', 'rcona575']]
    df_loans_exc_first_lien_domestic = df_loans_exc_first_lien_domestic.rename(columns={
        'rssd9001': 'Bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rcona570': '<3m',
        'rcona571': '3m-1y',
        'rcona572': '1y-3y',
        'rcona573': '3y-5y',
        'rcona574': '5y-15y',
        'rcona575': '>15y'
    })
    df_loans_exc_first_lien_domestic = df_loans_exc_first_lien_domestic.dropna()
    df_loans_exc_first_lien_domestic = df_loans_exc_first_lien_domestic[df_loans_exc_first_lien_domestic['report_date'] == report_date]

    df_other_loan = pd.concat([df_loans_exc_first_lien_domestic, df_loans_exc_first_lien])
    df_other_loan = df_other_loan.sort_index()

    return df_other_loan


def get_total_asset(rcfd_series_2, rcon_series_2, report_date = '03/31/2022'):

    #This grabs the
    asset_level_domestic_foriegn = rcfd_series_2[['rssd9001','rssd9017','rssd9999','rcfd2170']]
    asset_level_domestic = rcon_series_2[['rssd9001','rssd9017','rssd9999','rcon2170']]

    #drop the rows with missing values
    asset_level_domestic_foriegn.dropna(inplace = True)
    asset_level_domestic.dropna(inplace = True)

    filtered_asset_level_domestic_foriegn = asset_level_domestic_foriegn[asset_level_domestic_foriegn['rssd9999'] == report_date]
    filtered_asset_level_domestic = asset_level_domestic[asset_level_domestic['rssd9999'] == report_date]

    filtered_asset_level_domestic_foriegn  = filtered_asset_level_domestic_foriegn.rename(columns={
    'rcfd2170': 'Total Asset'})

    filtered_asset_level_domestic  = filtered_asset_level_domestic.rename(columns={
    'rcon2170': 'Total Asset'})

    df_asset = pd.concat([filtered_asset_level_domestic_foriegn, filtered_asset_level_domestic])

    df_asset = df_asset[['rssd9001','rssd9017','Total Asset']]

    df_asset  = df_asset.rename(columns={
    'rssd9001': 'Bank_ID',
    'rssd9017': 'bank_name',
    'rssd9999': 'report_date',
    'Total Asset': 'gross_asset',
    })

    return df_asset

def get_uninsured_deposits(rcon_series_1, report_date = '03/31/2022'):

    uninsured_deposit = rcon_series_1[['rssd9001','rssd9017', 'rssd9999', 'rcon5597']]

    uninsured_deposit = uninsured_deposit.rename(columns={
    'rssd9001': 'bank_ID',
    'rssd9017': 'bank_name',
    'rssd9999': 'report_date',
    'rcon5597': 'uninsured_deposit'

    })
    uninsured_deposit = uninsured_deposit[uninsured_deposit['report_date'] == report_date]

    return uninsured_deposit


def get_insured_deposits(rcon_series_1, report_date = '03/31/2022'):

    insured_deposit = rcon_series_1[['rssd9001','rssd9017', 'rssd9999', 'rconf049', 'rconf045']] 
    #RCFDF049 are Deposit accounts (excluding retirement accounts) of $250,000 or less
    #RCFDF045 are Retirement deposit accounts of $250,000 or less

    insured_deposit = insured_deposit.rename(columns={
        'rssd9001': 'bank_ID',
        'rssd9017': 'bank_name',
        'rssd9999': 'report_date',
        'rconf049': 'insured_deposit_1',
        'rconf045': 'insured_deposit_2'
    })

    insured_deposit = insured_deposit[insured_deposit['report_date'] == report_date]

    insured_deposit['insured_deposit'] = insured_deposit['insured_deposit_1'] + insured_deposit['insured_deposit_2']

    return insured_deposit


def clean_treasury_prices(treasury_prices, start_date = '2022-03-31', end_date = '2023-03-31'):

    treasury_prices = treasury_prices[['date', 'iShares 0-1', 'iShares 1-3', 'sp 3-5', 'iShares 7-10', 'iShares 10-20', 'iShares 20+']]
    treasury_prices = treasury_prices.set_index('date')
    treasury_prices = treasury_prices.resample('Q').first()
    treasury_prices = treasury_prices.loc[start_date:end_date]
    
    return treasury_prices

def clean_sp_treasury_bond_index(df_SP_Treasury_bond_index, start_date = '2022-03-31', end_date = '2023-03-31'):

    df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.set_index('date')
    df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.resample('Q').first()
    df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.loc[start_date:end_date]
    
    return df_SP_Treasury_bond_index

def clean_iShare_MBS_ETF(df_iShare_MBS_ETF, start_date = '2022-03-31', end_date = '2023-03-31'):

    df_iShare_MBS_ETF = df_iShare_MBS_ETF[['Date', 'Adj Close']]
    df_iShare_MBS_ETF['Date'] = pd.to_datetime(df_iShare_MBS_ETF['Date'])
    df_iShare_MBS_ETF.set_index('Date', inplace=True)
    df_iShare_MBS_ETF = df_iShare_MBS_ETF.resample('Q').first()
    df_iShare_MBS_ETF.index.rename('date', inplace=True)
    df_iShare_MBS_ETF = df_iShare_MBS_ETF.loc[start_date:end_date]
   
    return df_iShare_MBS_ETF
