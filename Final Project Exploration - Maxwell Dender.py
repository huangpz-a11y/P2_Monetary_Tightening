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

##Mark-to-market

#Treasury Prices
combined_index_df = pd.read_excel('../data/manual/combined_index_df.xlsx')
treasury_prices = combined_index_df[['date', 'iShares 0-1', 'iShares 1-3', 'sp 3-5', 'iShares 7-10', 'iShares 10-20', 'iShares 20+']]
treasury_prices = treasury_prices.set_index('date')
treasury_prices = treasury_prices.loc['2021-12-31':'2023-03-31']

#SP Tresasury Bond Index
df_SP_Treasury_bond_index = pd.read_excel(r'../data/manual/PerformanceGraphExport.xlsx')
df_SP_Treasury_bond_index['date'] = df_SP_Treasury_bond_index['date'].dt.strftime('%Y-%m-%d')
df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.set_index('date')
df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.loc['2021-12-31':'2023-03-31']

#iShare MBS ETF
df_iShare_MBS_ETF = pd.read_csv(r'../data/manual/MBB.csv')
df_iShare_MBS_ETF = df_iShare_MBS_ETF[['Date', 'Adj Close']]
df_iShare_MBS_ETF.set_index('Date', inplace = True)
df_iShare_MBS_ETF.index.rename('date', inplace = True)

#RMBS Multiplier
def RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF):
    upper_treasury = df_SP_Treasury_bond_index.loc['2023-03-31', 'S&P U.S. Treasury Bond Index']
    lower_treasury = df_SP_Treasury_bond_index.loc['2022-03-31', 'S&P U.S. Treasury Bond Index']

    upper_MBS = df_iShare_MBS_ETF.loc['2023-03-31', 'Adj Close']
    lower_MBS = df_iShare_MBS_ETF.loc['2022-03-31', 'Adj Close']

    MBS_change = (upper_MBS / lower_MBS) - 1
    treasury_change = (upper_treasury / lower_treasury) - 1
    multiplier = MBS_change / treasury_change

    return multiplier

RMBS_Multiplier = RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF)
RMBS_Multiplier

#Function to compute losses for all banks
def compute_all_bank_loss(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan,
                          treasury_prices, RMBS_multiplier):
    # Consolidate '<3m' and '3m-1y' into '<1y' for all DataFrames
    for df in [df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan]:
        df['<1y'] = df['<3m'] + df['3m-1y']

    # Calculate price changes for Treasury for each time bucket
    # price_change = {
    # '<1y': treasury_prices.loc['2023-03-31', 'iShares 0-1'] - treasury_prices.loc['2022-03-31', 'iShares 0-1'],
    # '1y-3y': treasury_prices.loc['2023-03-31', 'iShares 1-3'] - treasury_prices.loc['2022-03-31', 'iShares 1-3'],
    # '3y-5y': treasury_prices.loc['2023-03-31', 'sp 3-5'] - treasury_prices.loc['2022-03-31', 'sp 3-5'],
    # '7y-10y': treasury_prices.loc['2023-03-31', 'iShares 7-10'] - treasury_prices.loc['2022-03-31', 'iShares 7-10'],
    # '10y-20y': treasury_prices.loc['2023-03-31', 'iShares 10-20'] - treasury_prices.loc['2022-03-31', 'iShares 10-20'],
    # '>20y': treasury_prices.loc['2023-03-31', 'iShares 20+'] - treasury_prices.loc['2022-03-31', 'iShares 20+'],
    # }

    price_change = {
        '<1y': treasury_prices.loc['2023-03-31', 'iShares 0-1'] / treasury_prices.loc['2022-03-31', 'iShares 0-1'] - 1,
        '1y-3y': treasury_prices.loc['2023-03-31', 'iShares 1-3'] / treasury_prices.loc[
            '2022-03-31', 'iShares 1-3'] - 1,
        '3y-5y': treasury_prices.loc['2023-03-31', 'sp 3-5'] / treasury_prices.loc['2022-03-31', 'sp 3-5'] - 1,
        '7y-10y': treasury_prices.loc['2023-03-31', 'iShares 7-10'] / treasury_prices.loc[
            '2022-03-31', 'iShares 7-10'] - 1,
        '10y-20y': treasury_prices.loc['2023-03-31', 'iShares 10-20'] / treasury_prices.loc[
            '2022-03-31', 'iShares 10-20'] - 1,
        '>20y': treasury_prices.loc['2023-03-31', 'iShares 20+'] / treasury_prices.loc['2022-03-31', 'iShares 20+'] - 1,
    }

    # Map the time buckets from Treasury to the corresponding buckets in the other DataFrames
    bucket_mapping = {
        '<1y': '<1y',
        '1y-3y': '1y-3y',
        '3y-5y': '3y-5y',
        '7y-10y': '5y-15y',
        '10y-20y': '>15y',
        '>20y': '>15y'
    }

    # Function to compute the losses and calculate the median and sum of the losses
    def calculate_bank_losses(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan,
                              RMBS_multiplier, price_change, bucket_mapping):
        # Create a new DataFrame to store the losses for each bank
        bank_losses = pd.DataFrame(index=df_RMBS_Final['bank_name'])

        # Calculate losses for each type of asset
        for treasury_bucket, df_bucket in bucket_mapping.items():
            bank_losses[f'{treasury_bucket}_rmbs_loss'] = RMBS_multiplier * df_RMBS_Final.set_index('bank_name')[
                df_bucket] * price_change[treasury_bucket]
            bank_losses[f'{treasury_bucket}_first_lien_loss'] = RMBS_multiplier * \
                                                                df_loans_first_lien_domestic.set_index('bank_name')[
                                                                    df_bucket] * price_change[treasury_bucket]
            bank_losses[f'{treasury_bucket}_treasury_and_other_loss'] = df_treasury_and_others.set_index('bank_name')[
                                                                            df_bucket] * price_change[treasury_bucket]
            bank_losses[f'{treasury_bucket}_other_loans_loss'] = df_other_loan.set_index('bank_name')[df_bucket] * \
                                                                 price_change[treasury_bucket]

        # Sum the losses for each bank
        bank_losses['total_loss'] = bank_losses.sum(axis=1)

        # Calculate the median loss value among all banks
        median_loss = bank_losses['total_loss'].median()

        # Calculate the sum of the losses
        sum_loss = bank_losses['total_loss'].sum()

        # Return the median and sum of the losses
        return median_loss, sum_loss

    # Call the function with the required arguments
    median_loss, sum_loss = calculate_bank_losses(RMBS_all, first_lien_all, treasury_and_others_all,
                                                  other_loan_all, RMBS_multiplier, price_change, bucket_mapping)

    print(f"Median Loss All Banks: {median_loss}")
    print(f"Sum of Losses All Banks: {sum_loss}")

    #Call function with for GSIB Banks
    median_loss, sum_loss = calculate_bank_losses(RMBS_GSIB, first_lien_GSIB, treasury_and_other_GSIB,
                                                  other_loan_GSIB, RMBS_multiplier, price_change, bucket_mapping)

    print(f"Median Loss GSIB banks: {median_loss}")
    print(f"Sum of Losses GSIB banks: {sum_loss}")

    # Call function with for large non-GSIB Banks
    median_loss, sum_loss = calculate_bank_losses(RMBS_large_ex_GSIB, first_lien_large_ex_GSIB, treasury_and_other_large_ex_GSIB,
                                                  other_loan_large_ex_GSIB, RMBS_multiplier, price_change, bucket_mapping)

    print(f"Median Loss Large Banks excl. GSIB: {median_loss}")
    print(f"Sum of Losses Large Banks excl. GSIB: {sum_loss}")

    # Call function with for small Banks
    median_loss, sum_loss = calculate_bank_losses(RMBS_small, first_lien_small, treasury_and_other_small,
                                                  other_loan_small, RMBS_multiplier, price_change, bucket_mapping)

    print(f"Median Loss Small Banks: {median_loss}")
    print(f"Sum of Losses Small Banks: {sum_loss}")