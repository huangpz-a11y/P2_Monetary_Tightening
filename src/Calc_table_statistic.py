import pandas as pd
import load_WRDS
import load_assets
import config
import Clean_data

import numpy as np
from pathlib import Path


DATA_DIR = config.DATA_DIR
OUTPUT_DIR = config.OUTPUT_DIR

rcfd_series_1 = load_WRDS.load_RCFD_series_1(data_dir=DATA_DIR)
rcon_series_1 = load_WRDS.load_RCON_series_1(data_dir=DATA_DIR)
rcfd_series_2 = load_WRDS.load_RCFD_series_2(data_dir=DATA_DIR)
rcon_series_2 = load_WRDS.load_RCON_series_2(data_dir=DATA_DIR)

treasury_prices = pd.read_excel("./data/manual/combined_index_df.xlsx")
treasury_prices_1 = treasury_prices.copy()
df_SP_Treasury_bond_index = pd.read_excel("./data/manual/Treasury_Index.xlsx") 
df_SP_Treasury_bond_index_1 = df_SP_Treasury_bond_index.copy()
df_iShare_MBS_ETF = pd.read_csv("./data/manual/MBS_ETF.csv")
df_iShare_MBS_ETF_1 = df_iShare_MBS_ETF.copy()

def RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF, start_date = '2022-03-31', end_date = '2023-03-31'):
  
    upper_treasury = df_SP_Treasury_bond_index.loc[end_date, 'S&P U.S. Treasury Bond Index']
    lower_treasury = df_SP_Treasury_bond_index.loc[start_date, 'S&P U.S. Treasury Bond Index']
    
    upper_MBS = df_iShare_MBS_ETF.loc[end_date, 'Adj Close']
    lower_MBS = df_iShare_MBS_ETF.loc[start_date, 'Adj Close']
    
    MBS_change = (upper_MBS / lower_MBS) - 1
    treasury_change = (upper_treasury / lower_treasury) - 1
    multiplier = MBS_change / treasury_change
    
    return multiplier


def report_losses(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan, treasury_prices, RMBS_multiplier, df_asset, start_date = '2022-03-31', end_date = '2023-03-31'):        
    
    price_change = {
        '<1y': treasury_prices.loc[end_date, 'iShares 0-1'] / treasury_prices.loc[start_date, 'iShares 0-1'] - 1,
        '1y-3y': treasury_prices.loc[end_date, 'iShares 1-3'] / treasury_prices.loc[start_date, 'iShares 1-3'] - 1,
        '3y-5y': treasury_prices.loc[end_date, 'sp 3-5'] / treasury_prices.loc[start_date, 'sp 3-5'] - 1,
        '7y-10y': 0.5 * (treasury_prices.loc[end_date, 'iShares 7-10'] / treasury_prices.loc[start_date, 'iShares 7-10'] - 1) + 0.5 * (treasury_prices.loc[end_date, 'iShares 10-20'] / treasury_prices.loc[start_date, 'iShares 10-20'] - 1),
        '>20y': treasury_prices.loc[end_date, 'iShares 20+'] / treasury_prices.loc[start_date, 'iShares 20+'] - 1,
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
    for _, bank_loss_row in bank_losses_assets.iterrows():
        bank_name = bank_loss_row['bank_name']
        bank_id = bank_loss_row['bank_ID']
        
        # Adjust the lookup to include 'Bank_ID'
        uninsured_deposit_value = uninsured_lookup.get((bank_name, bank_id), 0)
        
        # Calculate 'MM Asset' as (as defined in the paper)
        mm_asset = bank_loss_row['total_loss'] + bank_loss_row['gross_asset']
        
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
        
        # Calculate mark-to-market asset value 
        mark_to_market_asset_value = bank_loss_row['total_loss'] + bank_loss_row['gross_asset']
        
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


def final_statistic_table(bank_losses_assets, uninsured_deposit_mm_asset, insured_deposit_coverage, index_name = 'All Banks'):
    # Merge the DataFrames on bank_name and Bank_ID to include uninsured deposit/MM Asset ratios and insured deposit coverage ratios
    
    
    bank_count = len(bank_losses_assets.index)

    final_stats = pd.DataFrame({
        'Aggregate Loss': [f"{-round(bank_losses_assets['total_loss'].sum() / 1e9, 1)}T"],  # Convert to trillions
        'Bank Level Loss': [f"{-round(bank_losses_assets['total_loss'].median() / 1e3, 1)}M"],  # Convert to millions
        'Bank Level Loss Std': [f"{round(bank_losses_assets['total_loss'].std() / 1e6, 2)}B"],  # Std deviation for Bank Level Loss
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
    final_stats.index = [index_name]

    final_stats = final_stats.T
    
    return final_stats

def GSIB_bank_id():
    #GSIB = [35301,93619,229913,398668,413208,451965,476810,480228,488318,
     #497404,541101,651448,688079,722777,812164,852218,934329,1225761,
     #1443266,1456501,2182786,2362458,2489805,2531991,3066025]
    GSIB = [852218, 480228, 476810, 413208, #JP Morgan, Bank of America, Citigroup, HSBC
      2980209, 2182786, 541101, 655839, 1015560, 229913,#Barclays, Goldman Sachs, BNY Mellon, CCB COMMUNITY BANK, ICBC, Mizuho
       1456501, 722777, 35301, 925411, 497404, 3212149, #Morgan Stanley, Santander, State Street, Sumitomo Mitsui, TD Bank, UBS
      451965] #wells fargo
    return GSIB

def large_ex_GSIB_bank_id(large):
    bank_id_large_ex_GSIB = []
    for bank_id in large['Bank_ID']:
       bank_id_large_ex_GSIB.append(bank_id)
    return bank_id_large_ex_GSIB

def small_bank_id(small):
    bank_id_small = []
    for bank_id in small['Bank_ID']:
       bank_id_small.append(bank_id)
    return bank_id_small

if __name__ == '__main__':

    ##Clean the dataframes for table 1##################################################################################################################################### 
    treasury_prices = Clean_data.clean_treasury_prices(treasury_prices, start_date = '2022-03-31', end_date = '2023-03-31')
    df_SP_Treasury_bond_index = Clean_data.clean_sp_treasury_bond_index(df_SP_Treasury_bond_index, start_date = '2022-03-31', end_date = '2023-03-31')
    df_iShare_MBS_ETF = Clean_data.clean_iShare_MBS_ETF(df_iShare_MBS_ETF, start_date = '2022-03-31', end_date = '2023-03-31')
    RMBS_multiplier = RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF, start_date = '2022-03-31', end_date = '2023-03-31') #MBS multiplier

    ##Prepare the dataframes for table 2 (with most up-to-date market indices data)##################################################################################################################################### 
    treasury_prices_updated = Clean_data.clean_treasury_prices(treasury_prices_1, start_date = '2022-03-31', end_date = '2023-12-31')
    df_SP_Treasury_bond_index_updated = Clean_data.clean_sp_treasury_bond_index(df_SP_Treasury_bond_index_1, start_date = '2022-03-31', end_date = '2023-12-31')
    df_iShare_MBS_ETF_updated = Clean_data.clean_iShare_MBS_ETF(df_iShare_MBS_ETF_1, start_date = '2022-03-31', end_date = '2023-12-31')
    RMBS_multiplier_updated = RMBs_Multiplier(df_SP_Treasury_bond_index_updated, df_iShare_MBS_ETF_updated, start_date = '2022-03-31', end_date = '2023-12-31') #MBS multiplier
    
    ##Get the required dataframes##################################################################################################################################### 
    df_RMBS_Final = Clean_data.get_RMBs(rcfd_series_1, rcon_series_1)
    df_loans_first_lien_domestic = Clean_data.get_loans(rcon_series_1)
    df_treasury_and_others = Clean_data.get_treasuries(rcfd_series_2, rcon_series_2)
    df_other_loan = Clean_data.get_other_loan(rcon_series_2, rcfd_series_1)
    df_asset = Clean_data.get_total_asset(rcfd_series_2, rcon_series_2)
    uninsured_deposit = Clean_data.get_uninsured_deposits(rcon_series_1)
    insured_deposits = Clean_data.get_insured_deposits(rcon_series_1)


    ##Sort the dataframes#####################################################################################################################################
    df_asset = df_asset #total assets all banks
    #GSIB Banks
    GSIB = GSIB_bank_id() #list of GSIB bank IDs
    df_asset_GSIB = df_asset[df_asset['Bank_ID'].isin(GSIB)] #total assets all GSIB banks
    #Large non-GSIB Banks
    df_asset_large_ex_GSIB = df_asset[(~df_asset['Bank_ID'].isin(GSIB)) & (df_asset['gross_asset']>1384000)] #total assets all large non-GSIB banks
    large_ex_GSIB = large_ex_GSIB_bank_id(df_asset_large_ex_GSIB) #list of large non-GSIB bank IDs
    #Small Banks
    df_asset_small = df_asset[(~df_asset['Bank_ID'].isin(GSIB)) & (df_asset['gross_asset']<=1384000)] #total asset all small banks 
    small = small_bank_id(df_asset_small) #list of small bank IDs


    ##Prepare each asset type###################################################################################################################################
    #RMBS
    df_RMBS_Final = df_RMBS_Final #RMBS for all banks 
    df_RMBS_GSIB = df_RMBS_Final[df_RMBS_Final['Bank_ID'].isin(GSIB)] #RMBS for GSIB banks
    df_RMBS_large_ex_GSIB = df_RMBS_Final[df_RMBS_Final['Bank_ID'].isin(large_ex_GSIB)] #RMBS for large non-GSIB banks
    df_RMBS_small = df_RMBS_Final[df_RMBS_Final['Bank_ID'].isin(small)] #RMBS for small banks

    #Loans First Lien Domestic

    df_loans_first_lien_domestic = df_loans_first_lien_domestic # loans first lien domestic for all banks
    df_loans_first_lien_domestic_GSIB = df_loans_first_lien_domestic[df_loans_first_lien_domestic['Bank_ID'].isin(GSIB)] # loans first lien domestic for all GSIB banks
    df_loans_first_lien_domestic_large_ex_GSIB = df_loans_first_lien_domestic[df_loans_first_lien_domestic['Bank_ID'].isin(large_ex_GSIB)] # loans first lien domestic for all large non-GSIB banks
    df_loans_first_lien_domestic_small = df_loans_first_lien_domestic[df_loans_first_lien_domestic['Bank_ID'].isin(small)]

    #Treasury and Others

    df_treasury_and_others = df_treasury_and_others #treasury and others all banks 
    df_treasury_and_others_GSIB = df_treasury_and_others[df_treasury_and_others['Bank_ID'].isin(GSIB)] #treasury and others GSIB banks
    df_treasury_and_others_large_ex_GSIB = df_treasury_and_others[df_treasury_and_others['Bank_ID'].isin(large_ex_GSIB)] #treasury and others large non-GSIB baanks 
    df_treasury_and_others_small = df_treasury_and_others[df_treasury_and_others['Bank_ID'].isin(small)] #treasury and others small banks 
    
    #Other Loan 

    df_other_loan = df_other_loan #other loans for all banks 
    df_other_loan_GSIB = df_other_loan[df_other_loan['Bank_ID'].isin(GSIB)] #other loans for all GSIB banks 
    df_other_loan_large_ex_GSIB = df_other_loan[df_other_loan['Bank_ID'].isin(large_ex_GSIB)] #other loans for all large non-GSIB banks
    df_other_loan_small = df_other_loan[df_other_loan['Bank_ID'].isin(small)] #other oans for all small banks 

    #uninsured deposits
    uninsured_deposit = uninsured_deposit #uninsured deposits for all banks
    uninsured_deposit_GSIB = uninsured_deposit[uninsured_deposit['bank_ID'].isin(GSIB)] #uninsured deposits for GSIB banks
    uninsured_deposit_large_ex_GSIB = uninsured_deposit[uninsured_deposit['bank_ID'].isin(large_ex_GSIB)] #uninsured deposits for large non-GSIB banks
    uninsured_deposit_small = uninsured_deposit[uninsured_deposit['bank_ID'].isin(small)] #uninsured deposits for small banks

    #insured deposits
    insured_deposits = insured_deposits #insured deposits for all banks
    insured_deposits_GSIB = insured_deposits[insured_deposits['bank_ID'].isin(GSIB)] #insured deposits for GSIB banks
    insured_deposits_large_ex_GSIB = insured_deposits[insured_deposits['bank_ID'].isin(large_ex_GSIB)] #insured deposits for large non-GSIB banks
    insured_deposits_small = insured_deposits[insured_deposits['bank_ID'].isin(small)] #insured deposits for small banks

    """
    The following code runs the statistics for table 1 (as in the paper)
    
    """

    ##Calculations for all banks##################################################################################################################################### 
    # Calculate the losses 
    bank_losses_assets = report_losses(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan, treasury_prices, RMBS_multiplier, df_asset)
    
    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset = calculate_uninsured_deposit_mm_asset(uninsured_deposit, bank_losses_assets)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage = insured_deposit_coverage_ratio(insured_deposits, uninsured_deposit, bank_losses_assets)
    
    # Calculate the final statistics table
    final_stats = final_statistic_table(bank_losses_assets, uninsured_deposit_mm_asset, insured_deposit_coverage)
    
    ##################################################################################################################################################################

    ##Calculations for all GSIB banks################################################################################################################################
    # Calculate the losses 
    bank_losses_assets_GSIB = report_losses(df_RMBS_GSIB, df_loans_first_lien_domestic_GSIB, df_treasury_and_others_GSIB, df_other_loan_GSIB, treasury_prices, RMBS_multiplier, df_asset_GSIB)
    
    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_GSIB = calculate_uninsured_deposit_mm_asset(uninsured_deposit_GSIB, bank_losses_assets_GSIB)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_GSIB = insured_deposit_coverage_ratio(insured_deposits_GSIB, uninsured_deposit_GSIB, bank_losses_assets_GSIB)
    
    # Calculate the final statistics table
    final_stats_GSIB = final_statistic_table(bank_losses_assets_GSIB, uninsured_deposit_mm_asset_GSIB, insured_deposit_coverage_GSIB, index_name = 'GSIB Banks')
    ##################################################################################################################################################################

    ##Calculations for all Large non-GSIB banks################################################################################################################################
    # Calculate the losses 
    bank_losses_assets_large_ex_GSIB = report_losses(df_RMBS_large_ex_GSIB, df_loans_first_lien_domestic_large_ex_GSIB, df_treasury_and_others_large_ex_GSIB, df_other_loan_large_ex_GSIB, treasury_prices, RMBS_multiplier, df_asset_large_ex_GSIB)
    
    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_large_ex_GSIB = calculate_uninsured_deposit_mm_asset(uninsured_deposit_large_ex_GSIB, bank_losses_assets_large_ex_GSIB)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_large_ex_GSIB = insured_deposit_coverage_ratio(insured_deposits_large_ex_GSIB, uninsured_deposit_large_ex_GSIB, bank_losses_assets_large_ex_GSIB)
    
    # Calculate the final statistics table
    final_stats_large_ex_GSIB = final_statistic_table(bank_losses_assets_large_ex_GSIB, uninsured_deposit_mm_asset_large_ex_GSIB, insured_deposit_coverage_large_ex_GSIB, index_name = 'Large Ex GSIB Banks')
    ##################################################################################################################################################################

    ##Calculations for small banks################################################################################################################################
    # Calculate the losses 
    bank_losses_assets_small = report_losses(df_RMBS_small, df_loans_first_lien_domestic_small, df_treasury_and_others_small, df_other_loan_small, treasury_prices, RMBS_multiplier, df_asset_small)
    
    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_small = calculate_uninsured_deposit_mm_asset(uninsured_deposit_small, bank_losses_assets_small)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_small = insured_deposit_coverage_ratio(insured_deposits_small, uninsured_deposit_small, bank_losses_assets_small)
    
    # Calculate the final statistics table
    final_stats_small = final_statistic_table(bank_losses_assets_small, uninsured_deposit_mm_asset_small, insured_deposit_coverage_small, index_name = 'Small Banks')
    ##################################################################################################################################################################

    table_1 = pd.concat([final_stats, final_stats_small, final_stats_large_ex_GSIB, final_stats_GSIB], axis=1)

    # Sets format for printing to LaTeX
    float_format_func = lambda x: '{:.1f}'.format(x)
    latex_table_string = table_1.to_latex(float_format=float_format_func)
    path = OUTPUT_DIR / f'Table1.tex'
    with open(path, "w") as text_file:
        text_file.write(latex_table_string)


    print(table_1)

    """
    The following code runs the statistics for table 2 (with updated numbers for market indices that are used for market to market calculations, updated to 2023-12-31)
    
    """
     ##Calculations for all banks##################################################################################################################################### 
    # Calculate the losses
    bank_losses_assets_updated = report_losses(df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan, treasury_prices_updated, RMBS_multiplier_updated, df_asset)

    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_updated = calculate_uninsured_deposit_mm_asset(uninsured_deposit, bank_losses_assets_updated)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_updated = insured_deposit_coverage_ratio(insured_deposits, uninsured_deposit, bank_losses_assets_updated)

    # Calculate the final statistics table
    final_stats_updated = final_statistic_table(bank_losses_assets_updated, uninsured_deposit_mm_asset_updated, insured_deposit_coverage_updated)

    ##################################################################################################################################################################

    ##Calculations for all GSIB banks################################################################################################################################
    # Calculate the losses
    bank_losses_assets_GSIB_updated = report_losses(df_RMBS_GSIB, df_loans_first_lien_domestic_GSIB, df_treasury_and_others_GSIB, df_other_loan_GSIB, treasury_prices_updated, RMBS_multiplier_updated, df_asset_GSIB)

    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_GSIB_updated = calculate_uninsured_deposit_mm_asset(uninsured_deposit_GSIB, bank_losses_assets_GSIB_updated)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_GSIB_updated = insured_deposit_coverage_ratio(insured_deposits_GSIB, uninsured_deposit_GSIB, bank_losses_assets_GSIB_updated)

    # Calculate the final statistics table
    final_stats_GSIB_updated = final_statistic_table(bank_losses_assets_GSIB_updated, uninsured_deposit_mm_asset_GSIB_updated, insured_deposit_coverage_GSIB_updated, index_name='GSIB Banks')


    ##################################################################################################################################################################

    ##Calculations for all Large non-GSIB banks################################################################################################################################
    # Calculate the losses
    bank_losses_assets_large_ex_GSIB_updated = report_losses(df_RMBS_large_ex_GSIB, df_loans_first_lien_domestic_large_ex_GSIB, df_treasury_and_others_large_ex_GSIB, df_other_loan_large_ex_GSIB, treasury_prices_updated, RMBS_multiplier_updated, df_asset_large_ex_GSIB)

    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_large_ex_GSIB_updated = calculate_uninsured_deposit_mm_asset(uninsured_deposit_large_ex_GSIB, bank_losses_assets_large_ex_GSIB_updated)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_large_ex_GSIB_updated = insured_deposit_coverage_ratio(insured_deposits_large_ex_GSIB, uninsured_deposit_large_ex_GSIB, bank_losses_assets_large_ex_GSIB_updated)

    # Calculate the final statistics table
    final_stats_large_ex_GSIB_updated = final_statistic_table(bank_losses_assets_large_ex_GSIB_updated, uninsured_deposit_mm_asset_large_ex_GSIB_updated, insured_deposit_coverage_large_ex_GSIB_updated, index_name='Large Ex GSIB Banks')

    ##################################################################################################################################################################


    ##Calculations for small banks################################################################################################################################

    # Calculate the losses
    bank_losses_assets_small_updated = report_losses(df_RMBS_small, df_loans_first_lien_domestic_small, df_treasury_and_others_small, df_other_loan_small, treasury_prices_updated, RMBS_multiplier_updated, df_asset_small)

    # Calculate the uninsured deposit/MM asset ratio
    uninsured_deposit_mm_asset_small_updated = calculate_uninsured_deposit_mm_asset(uninsured_deposit_small, bank_losses_assets_small_updated)

    # Calculate the insured deposit coverage ratio
    insured_deposit_coverage_small_updated = insured_deposit_coverage_ratio(insured_deposits_small, uninsured_deposit_small, bank_losses_assets_small_updated)

    # Calculate the final statistics table
    final_stats_small_updated = final_statistic_table(bank_losses_assets_small_updated, uninsured_deposit_mm_asset_small_updated, insured_deposit_coverage_small_updated, index_name='Small Banks')

    ##################################################################################################################################################################

    table_2 = pd.concat([final_stats_updated, final_stats_small_updated, final_stats_large_ex_GSIB_updated, final_stats_GSIB_updated], axis=1)

    # Sets format for printing to LaTeX
    float_format_func = lambda x: '{:.1f}'.format(x)
    latex_table_string = table_2.to_latex(float_format=float_format_func)
    path = OUTPUT_DIR / f'Table2.tex'
    with open(path, "w") as text_file:
        text_file.write(latex_table_string)

    print(table_2)