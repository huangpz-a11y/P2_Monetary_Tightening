import pandas as pd
import load_WRDS
import config

DATA_DIR = config.DATA_DIR
OUTPUT_DIR = config.OUTPUT_DIR

rcfd_series_1 = load_WRDS.load_RCFD_series_1(data_dir=DATA_DIR)
rcon_series_1 = load_WRDS.load_RCON_series_1(data_dir=DATA_DIR)
rcfd_series_2 = load_WRDS.load_RCFD_series_2(data_dir=DATA_DIR)
rcon_series_2 = load_WRDS.load_RCON_series_2(data_dir=DATA_DIR)

treasury_prices = pd.read_excel("./data/manual/combined_index_df.xlsx")
df_SP_Treasury_bond_index = pd.read_excel("./data/manual/PerformanceGraphExport.xlsx")
df_iShare_MBS_ETF = pd.read_csv("./data/manual/MBB.csv")

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


def clean_treasury_prices(treasury_prices):

    treasury_prices = treasury_prices[['date', 'iShares 0-1', 'iShares 1-3', 'sp 3-5', 'iShares 7-10', 'iShares 10-20', 'iShares 20+']]
    treasury_prices = treasury_prices.set_index('date')
    treasury_prices = treasury_prices.resample('Q').first()
    treasury_prices = treasury_prices.loc['2022-03-31':'2023-03-31']
    
    return treasury_prices

def clean_sp_treasury_bond_index(df_SP_Treasury_bond_index):

    df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.set_index('date')
    df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.resample('Q').first()
    df_SP_Treasury_bond_index = df_SP_Treasury_bond_index.loc['2022-03-31':'2023-03-31']
    
    return df_SP_Treasury_bond_index

def clean_iShare_MBS_ETF(df_iShare_MBS_ETF):

    df_iShare_MBS_ETF = df_iShare_MBS_ETF[['Date', 'Adj Close']]
    df_iShare_MBS_ETF['Date'] = pd.to_datetime(df_iShare_MBS_ETF['Date'])
    df_iShare_MBS_ETF.set_index('Date', inplace=True)
    df_iShare_MBS_ETF = df_iShare_MBS_ETF.resample('Q').first()
    df_iShare_MBS_ETF.index.rename('date', inplace=True)
    df_iShare_MBS_ETF = df_iShare_MBS_ETF.loc['2022-03-31':'2023-03-31']
   
    return df_iShare_MBS_ETF


def RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF, start_date = '2022-03-31', end_date = '2023-03-31'):
  
    upper_treasury = df_SP_Treasury_bond_index.loc[end_date, 'S&P U.S. Treasury Bond Index']
    lower_treasury = df_SP_Treasury_bond_index.loc[start_date, 'S&P U.S. Treasury Bond Index']
    
    upper_MBS = df_iShare_MBS_ETF.loc[end_date, 'Adj Close']
    lower_MBS = df_iShare_MBS_ETF.loc[start_date, 'Adj Close']
    
    MBS_change = (upper_MBS / lower_MBS) - 1
    treasury_change = (upper_treasury / lower_treasury) - 1
    multiplier = MBS_change / treasury_change
    
    return multiplier


def report_losses(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan, treasury_prices, RMBS_multiplier, df_asset):        
    
    price_change = {
        '<1y': treasury_prices.loc['2023-03-31', 'iShares 0-1'] / treasury_prices.loc['2022-03-31', 'iShares 0-1'] - 1,
        '1y-3y': treasury_prices.loc['2023-03-31', 'iShares 1-3'] / treasury_prices.loc['2022-03-31', 'iShares 1-3'] - 1,
        '3y-5y': treasury_prices.loc['2023-03-31', 'sp 3-5'] / treasury_prices.loc['2022-03-31', 'sp 3-5'] - 1,
        '7y-10y': 0.5 * (treasury_prices.loc['2023-03-31', 'iShares 7-10'] / treasury_prices.loc['2022-03-31', 'iShares 7-10'] - 1) + 0.5 * (treasury_prices.loc['2023-03-31', 'iShares 10-20'] / treasury_prices.loc['2022-03-31', 'iShares 10-20'] - 1),
        '>20y': treasury_prices.loc['2023-03-31', 'iShares 20+'] / treasury_prices.loc['2022-03-31', 'iShares 20+'] - 1,
    }

    bucket_mapping = {
        '<3m': '<1y',
        '3m-1y': '<1y',
        '1y-3y': '1y-3y',
        '3y-5y': '3y-5y',
        '5y-15y': '7y-10y',  # Assuming '5y-15y' should be mapped to '7y-10y' based on provided price_change calculation
        '>15y': '>20y',
    }
    
    aggregated_assets = {}
    for name, df in zip(['RMBS', 'Loans', 'Treasury', 'OtherLoan'], 
                        [df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan]):
        # Ensure columns for aggregation are present
        columns_to_aggregate = [col for col in list(bucket_mapping.keys()) if col in df.columns]
        aggregated_assets[name] = df.groupby(['bank_name', 'Bank_ID'])[columns_to_aggregate].sum().reset_index()
    
    # Initialize DataFrame to store results
    bank_losses_assets = pd.DataFrame(columns=[
        'bank_name', 'bank_ID', 'RMBs_loss', 'treasury_loss', 'loans_loss', 'other_loan_loss', 
        'total_loss', 'Share RMBs', 'Share Treasury and Other', 
        'Share Residential Mortgage', 'Share Other Loan', 'RMBs_asset', 'treasury_asset', 
        'residential_mortgage_asset', 'other_loan_asset', 'core_asset', 'gross_asset', 'loss/core_asset', 'loss/gross_asset',
    ])
    
    for _, df_row in df_asset.iterrows():
        bank = df_row['bank_name']
        bank_id = df_row['Bank_ID']
        bank_total_asset = df_row['gross_asset']
        
        #Initialize variables for loss and asset calculations
        rmbs_loss = loans_loss = treasury_loss = other_loan_loss = total_loss = 0
        rmbs_asset = treasury_asset = loan_asset = other_loan_asset = core_asset = 0
        
        #Calculating losses for RMBs
        if 'RMBS' in aggregated_assets and not aggregated_assets['RMBS'].empty:
            rmbs_row = aggregated_assets['RMBS'][(aggregated_assets['RMBS']['bank_name'] == bank) & (aggregated_assets['RMBS']['Bank_ID'] == bank_id)]
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in rmbs_row.columns:
                    asset_amount = rmbs_row.iloc[0][bucket] if not rmbs_row.empty else 0
                    rmbs_loss += (asset_amount * RMBS_multiplier * price_change[treasury_bucket])
                    rmbs_asset += asset_amount
                    
        #Calculating losses for loans
        loans_row = aggregated_assets['Loans'][(aggregated_assets['Loans']['bank_name'] == bank) & (aggregated_assets['Loans']['Bank_ID'] == bank_id)]
        if not loans_row.empty:
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in loans_row.columns:
                    asset_amount = loans_row.iloc[0][bucket]
                    loans_loss += (asset_amount * RMBS_multiplier * price_change[treasury_bucket])
                    loan_asset += asset_amount

        #Calculating Treasuries
        treasury_row = aggregated_assets['Treasury'][(aggregated_assets['Treasury']['bank_name'] == bank) & (aggregated_assets['Treasury']['Bank_ID'] == bank_id)]
        if not treasury_row.empty:
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in treasury_row.columns:
                    asset_amount = treasury_row.iloc[0][bucket]
                    treasury_loss += (asset_amount * price_change[treasury_bucket])
                    treasury_asset += asset_amount

        #Other loans
        other_loan_row = aggregated_assets['OtherLoan'][(aggregated_assets['OtherLoan']['bank_name'] == bank) & (aggregated_assets['OtherLoan']['Bank_ID'] == bank_id)]
        if not other_loan_row.empty:
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in other_loan_row.columns:
                    asset_amount = other_loan_row.iloc[0][bucket]
                    other_loan_loss += (asset_amount * price_change[treasury_bucket])
                    other_loan_asset += asset_amount
                
        total_loss = rmbs_loss + treasury_loss + loans_loss + other_loan_loss
        core_asset = rmbs_asset + treasury_asset + loan_asset + other_loan_asset

        bank_losses_assets.loc[len(bank_losses_assets)] = {
            'bank_name': bank,
            'bank_ID': bank_id,
            'RMBs_loss': rmbs_loss,
            'treasury_loss': treasury_loss,
            'loans_loss': loans_loss,
            'other_loan_loss': other_loan_loss,
            'total_loss': total_loss,
            'Share RMBs': rmbs_loss / total_loss if total_loss else 0,
            'Share Treasury and Other': treasury_loss / total_loss if total_loss else 0,
            'Share Residential Mortgage': loans_loss / total_loss if total_loss else 0,
            'Share Other Loan': other_loan_loss / total_loss if total_loss else 0,
            'RMBs_asset': rmbs_asset,
            'treasury_asset': treasury_asset,
            'residential_mortgage_asset': loan_asset,
            'other_loan_asset': other_loan_asset,
            'core_asset': core_asset,
            'gross_asset': bank_total_asset,
            'loss/core_asset': -(total_loss / core_asset) if core_asset else 0,
            'loss/gross_asset': -(total_loss / bank_total_asset) if bank_total_asset else 0,
        }

    return bank_losses_assets


def calculate_uninsured_deposit_mm_asset(uninsured_deposit, bank_losses_assets):
    
    # Initialize an empty list to store the results
    results = []
    
    # Adjust the uninsured_deposit DataFrame to use both 'bank_name' and 'Bank_ID' as a multi-index for quick lookup
    uninsured_lookup = uninsured_deposit.set_index(['bank_name', 'bank_ID'])['uninsured_deposit'].to_dict()
    
    # Iterate over each row in bank_losses DataFrame
    for index, bank_loss_row in bank_losses_assets.iterrows():
        bank_name = bank_loss_row['bank_name']
        bank_id = bank_loss_row['bank_ID']
        
        # Adjust the lookup to include 'Bank_ID'
        uninsured_deposit_value = uninsured_lookup.get((bank_name, bank_id), 0)
        
        # Calculate 'MM Asset' as the sum of 'total_loss' and 'gross_asset' (as defined in the paper)
        mm_asset = - bank_loss_row['total_loss'] + bank_loss_row['gross_asset']
        
        # Calculate Uninsured Deposit/MM Asset ratio 
        if mm_asset > 0:
            uninsured_deposit_mm_asset_ratio = uninsured_deposit_value / mm_asset
        
        # Append to final dataframe
        results.append({
            'bank_name': bank_name,
            'bank_ID': bank_id, 
            'total_loss': bank_loss_row['total_loss'], 
            'total_asset': bank_loss_row['gross_asset'],
            'mm_asset': mm_asset,
            'uninsured_deposit': uninsured_deposit_value, 
            'Uninsured_Deposit_MM_Asset': uninsured_deposit_mm_asset_ratio
        })

    # Convert results list to DataFrame and sort by 'Bank_ID'
    uninsured_deposit_mm_asset = pd.DataFrame(results).sort_values(by=['bank_name', 'bank_ID'])
    
    return uninsured_deposit_mm_asset


# Calculate the insured deposit coverage ratio, IGNORE as I need to go back and fix this logic later
def insured_deposit_coverage_ratio(insured_deposit, uninsured_deposit, bank_losses):
    # Initialize an empty list to store the results
    results = []
    
    # Create dictionaries from insured and uninsured deposits for quick lookup
    insured_lookup = insured_deposit.set_index(['bank_name', 'bank_ID'])['insured_deposit'].to_dict()
    uninsured_lookup = uninsured_deposit.set_index(['bank_name', 'bank_ID'])['uninsured_deposit'].to_dict()
    
    # Iterate over each row in bank_losses DataFrame
    for _, bank_loss_row in bank_losses.iterrows():
        bank_name = bank_loss_row['bank_name']
        bank_id = bank_loss_row['bank_ID']
        
        # Retrieve insured and uninsured deposit values
        insured_deposit_value = insured_lookup.get((bank_name, bank_id), 0)
        uninsured_deposit_value = uninsured_lookup.get((bank_name, bank_id), 0)
        
        # Calculate mark-to-market asset value as the sum of 'total_asset' minus 'total_loss'
        mark_to_market_asset_value = bank_loss_row['gross_asset'] + bank_loss_row['total_loss']
        
        # Calculate the insured deposit coverage ratio
        if insured_deposit_value > 0:  # Prevent division by zero
            coverage_ratio = (mark_to_market_asset_value - uninsured_deposit_value - insured_deposit_value) / insured_deposit_value
        
        # Append the result
        results.append({
            'bank_name': bank_name,
            'bank_ID': bank_id,
            'mm_asset': mark_to_market_asset_value,
            'insured_deposit': insured_deposit_value,
            'uninsured_deposit': uninsured_deposit_value,
            'insured_deposit_coverage_ratio': coverage_ratio
        })
    
    # Convert results list to DataFrame
    results_df = pd.DataFrame(results)
    
    return results_df


def final_statistic_table(bank_losses_assets, uninsured_deposit_mm_asset, insured_deposit_coverage):
    # Merge the DataFrames on bank_name and Bank_ID to include uninsured deposit/MM Asset ratios and insured deposit coverage ratios
    
    
    bank_count = len(bank_losses_assets.index)

    final_stats = pd.DataFrame({
        'Aggregate Loss': [f"{-round(bank_losses_assets['total_loss'].sum() / 1e9, 1)}T"],  # Convert to trillions
        'Bank Level Loss': [f"{-round(bank_losses_assets['total_loss'].median() / 1e3, 1)}M"],  # Convert to millions
        'Bank Level Loss Std': [f"{round(bank_losses_assets['total_loss'].std() / 1e6, 1)}B"],  # Std deviation for Bank Level Loss
        'Share RMBS': [round(bank_losses_assets['Share RMBs'].median() * 100, 1)],  # Median percentage
        'Share RMBS Std': [round(bank_losses_assets['Share RMBs'].std() * 100, 1)],  # Std deviation for Share RMBS
        'Share Treasury and Other': [round(bank_losses_assets['Share Treasury and Other'].median() * 100, 1)],  # Median percentage
        'Share Treasury and Other Std': [round(bank_losses_assets['Share Treasury and Other'].std() * 100, 1)],  # Std deviation
        'Share Residential Mortgage': [round(bank_losses_assets['Share Residential Mortgage'].median() * 100, 1)],  # Median percentage
        'Share Residential Mortgage Std': [round(bank_losses_assets['Share Residential Mortgage'].std() * 100, 1)],  # Std deviation
        'Share Other Loan': [round(bank_losses_assets['Share Other Loan'].median() * 100, 1)],  # Median percentage
        'Share Other Loan Std': [round(bank_losses_assets['Share Other Loan'].std() * 100, 1)],  # Std deviation
        'Loss/Asset': [round(bank_losses_assets['loss/gross_asset'].median() * 100, 1)],  # Median percentage
        'Loss/Asset Std': [round(bank_losses_assets['loss/gross_asset'].std() * 100, 1)],  # Std deviation
        'Uninsured Deposit/MM Asset': [round(uninsured_deposit_mm_asset['Uninsured_Deposit_MM_Asset'].median() * 100, 1)],  # Median percentage
        'Uninsured Deposit/MM Asset Std': [round(uninsured_deposit_mm_asset['Uninsured_Deposit_MM_Asset'].std() * 100, 1)],  # Std deviation
        'Insured Deposit Coverage Ratio': [round(insured_deposit_coverage['insured_deposit_coverage_ratio'].median() * 100, 1)],  # Median percentage
        'Insured Deposit Coverage Ratio Std': [round(insured_deposit_coverage['insured_deposit_coverage_ratio'].std() * 100, 1)],  # Std deviation
        'Number of Banks': [len(bank_losses_assets.index.unique())]  # Count of unique banks
    })

    # Rename index to 'All Banks'
    final_stats.index = ['All Banks']

    final_stats = final_stats.T
    
    return final_stats

if __name__ == '__main__':


    # Clean the dataframes
    treasury_prices = clean_treasury_prices(treasury_prices)
    df_SP_Treasury_bond_index = clean_sp_treasury_bond_index(df_SP_Treasury_bond_index)
    df_iShare_MBS_ETF = clean_iShare_MBS_ETF(df_iShare_MBS_ETF)

    # Calculate the multiplier for RMBS
    RMBS_multiplier = RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF)
    
    # Get the required dataframes
    df_RMBS_Final = get_RMBs(rcfd_series_1, rcon_series_1)
    df_loans_first_lien_domestic = get_loans(rcon_series_1)
    df_treasury_and_others = get_treasuries(rcfd_series_2, rcon_series_2)
    df_other_loan = get_other_loan(rcon_series_2, rcfd_series_1)
    df_asset = get_total_asset(rcfd_series_2, rcon_series_2)
    uninsured_deposit = get_uninsured_deposits(rcon_series_1)
    insured_deposits = get_insured_deposits(rcon_series_1)
    
    # Calculate the losses
    bank_losses_assets = report_losses(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan, treasury_prices, RMBS_multiplier, df_asset)
    
    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset = calculate_uninsured_deposit_mm_asset(uninsured_deposit, bank_losses_assets)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage = insured_deposit_coverage_ratio(insured_deposits, uninsured_deposit, bank_losses_assets)
    
    # Calculate the final statistics table
    final_stats = final_statistic_table(bank_losses_assets, uninsured_deposit_mm_asset, insured_deposit_coverage)
    
    print(final_stats)


