import pandas as pd

def RMBs_Multiplier(df_SP_Treasury_bond_index, df_iShare_MBS_ETF,inital_date,analysis_date):
    """
    Calculate the multiplier for RMBS assets based on the change in MBS and Treasury bond prices.

    Parameters:
    df_SP_Treasury_bond_index (DataFrame): DataFrame containing S&P U.S. Treasury Bond Index data
    df_iShare_MBS_ETF (DataFrame): DataFrame containing iShares MBS ETF data

    Returns:
    float: The calculated multiplier
    """
  
    upper_treasury = df_SP_Treasury_bond_index.loc[analysis_date, 'S&P U.S. Treasury Bond Index']
    lower_treasury = df_SP_Treasury_bond_index.loc[inital_date, 'S&P U.S. Treasury Bond Index']
    
    upper_MBS = df_iShare_MBS_ETF.loc[analysis_date, 'Adj Close']
    lower_MBS = df_iShare_MBS_ETF.loc[inital_date, 'Adj Close']
    
    MBS_change = (upper_MBS / lower_MBS) - 1
    treasury_change = (upper_treasury / lower_treasury) - 1
    multiplier = MBS_change / treasury_change
    
    return multiplier

def report_losses(inital_date,analysis_date,df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan, treasury_prices, RMBS_multiplier, gross_asset):
    """
    Calculate the losses for each bank based on the provided data and assumptions.

    Parameters:
    inital_date (str): The initial date for analysis
    analysis_date (str): The date for analysis
    df_RMBS_Final (DataFrame): DataFrame containing RMBS data
    df_loans_first_lien_domestic (DataFrame): DataFrame containing domestic first lien loans data
    df_treasury_and_others (DataFrame): DataFrame containing treasury and other assets data
    df_other_loan (DataFrame): DataFrame containing other loan data
    treasury_prices (DataFrame): DataFrame containing treasury prices data
    RMBS_multiplier (float): The multiplier for RMBS assets
    gross_asset (DataFrame): DataFrame containing gross asset data

    Returns:
    DataFrame: A DataFrame containing the calculated losses for each bank and associate assets
    """
    
    # Calculate the price change for each treasury bond category
    price_change = {
        '<1y': treasury_prices.loc[analysis_date, 'iShares 0-1'] / treasury_prices.loc[inital_date, 'iShares 0-1'] - 1,
        '1y-3y': treasury_prices.loc[analysis_date, 'iShares 1-3'] / treasury_prices.loc[inital_date, 'iShares 1-3'] - 1,
        '3y-5y': treasury_prices.loc[analysis_date, 'sp 3-5'] / treasury_prices.loc[inital_date, 'sp 3-5'] - 1,
        '7y-10y': 0.5 * (treasury_prices.loc[analysis_date, 'iShares 7-10'] / treasury_prices.loc[inital_date, 'iShares 7-10'] - 1) \
              + 0.5 * (treasury_prices.loc[analysis_date, 'iShares 10-20'] / treasury_prices.loc[inital_date, 'iShares 10-20'] - 1),
        '>20y': treasury_prices.loc[analysis_date, 'iShares 20+'] / treasury_prices.loc[inital_date, 'iShares 20+'] - 1,
    }

    # Define the mapping of buckets to be used for aggregation
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
    
    # Iterate over each row in gross_asset DataFrame
    for _, gross_row in gross_asset.iterrows():
        bank = gross_row['bank_name']
        bank_id = gross_row['Bank_ID']
        bank_gross_asset = gross_row['gross_asset']
        
        # Initialize variables for loss and asset calculations
        rmbs_loss = loans_loss = treasury_loss = other_loan_loss = total_loss = 0
        rmbs_asset = treasury_asset = loan_asset = other_loan_asset = core_asset = 0
        
        # Process RMBS assets
        if 'RMBS' in aggregated_assets and not aggregated_assets['RMBS'].empty:
            rmbs_row = aggregated_assets['RMBS'][(aggregated_assets['RMBS']['bank_name'] == bank) & (aggregated_assets['RMBS']['Bank_ID'] == bank_id)]
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in rmbs_row.columns:
                    asset_amount = rmbs_row.iloc[0][bucket] if not rmbs_row.empty else 0
                    rmbs_loss += (asset_amount * RMBS_multiplier * price_change[treasury_bucket])
                    rmbs_asset += asset_amount
                    
        # Loans
        loans_row = aggregated_assets['Loans'][(aggregated_assets['Loans']['bank_name'] == bank) & (aggregated_assets['Loans']['Bank_ID'] == bank_id)]
        if not loans_row.empty:
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in loans_row.columns:
                    asset_amount = loans_row.iloc[0][bucket]
                    loans_loss += (asset_amount * RMBS_multiplier * price_change[treasury_bucket])
                    loan_asset += asset_amount

        # Treasury
        treasury_row = aggregated_assets['Treasury'][(aggregated_assets['Treasury']['bank_name'] == bank) & (aggregated_assets['Treasury']['Bank_ID'] == bank_id)]
        if not treasury_row.empty:
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in treasury_row.columns:
                    asset_amount = treasury_row.iloc[0][bucket]
                    treasury_loss += (asset_amount * price_change[treasury_bucket])
                    treasury_asset += asset_amount

        # OtherLoan
        other_loan_row = aggregated_assets['OtherLoan'][(aggregated_assets['OtherLoan']['bank_name'] == bank) & (aggregated_assets['OtherLoan']['Bank_ID'] == bank_id)]
        if not other_loan_row.empty:
            for bucket, treasury_bucket in bucket_mapping.items():
                if bucket in other_loan_row.columns:
                    asset_amount = other_loan_row.iloc[0][bucket]
                    other_loan_loss += (asset_amount * price_change[treasury_bucket])
                    other_loan_asset += asset_amount
                
        # Calculate total loss and core asset
        total_loss = rmbs_loss + treasury_loss + loans_loss + other_loan_loss
        core_asset = rmbs_asset + treasury_asset + loan_asset + other_loan_asset

        # Append the results to the DataFrame
        bank_losses_assets.loc[len(bank_losses_assets)] = {
            'bank_name': bank,
            'bank_ID': bank_id,
            'RMBs_loss': rmbs_loss,
            'treasury_loss': treasury_loss,
            'loans_loss': loans_loss,
            'other_loan_loss': other_loan_loss,
            'total_loss': total_loss,
            'Share RMBs': 100 * rmbs_loss / total_loss if total_loss else 0,
            'Share Treasury and Other': 100 * treasury_loss / total_loss if total_loss else 0,
            'Share Residential Mortgage': 100 * loans_loss / total_loss if total_loss else 0,
            'Share Other Loan': 100 * other_loan_loss / total_loss if total_loss else 0,
            'RMBs_asset': rmbs_asset,
            'treasury_asset': treasury_asset,
            'residential_mortgage_asset': loan_asset,
            'other_loan_asset': other_loan_asset,
            'core_asset': core_asset,
            'gross_asset': bank_gross_asset,
            'loss/core_asset': -(total_loss / core_asset) if core_asset else 0,
            'loss/gross_asset': -(total_loss / bank_gross_asset) if bank_gross_asset else 0,
        }

    return bank_losses_assets

def calculate_uninsured_deposit_mm_asset(uninsured_deposit, bank_losses):
    """
    Calculate the Uninsured Deposit/MM Asset ratio for each bank based on the provided data.

    Parameters:
    uninsured_deposit (DataFrame): DataFrame containing uninsured deposit data
    bank_losses (DataFrame): DataFrame containing bank losses data

    Returns:
    DataFrame: A DataFrame containing the calculated Uninsured Deposit/MM Asset ratio for each bank
    """
    
    # Initialize an empty list to store the results
    results = []
    
    # Adjust the uninsured_deposit DataFrame to use both 'bank_name' and 'Bank_ID' as a multi-index for quick lookup
    uninsured_lookup = uninsured_deposit.set_index(['bank_name', 'bank_ID'])['uninsured_deposit'].to_dict()
    
    # Iterate over each row in bank_losses DataFrame
    for index, bank_loss_row in bank_losses.iterrows():
        bank_name = bank_loss_row['bank_name']
        bank_id = bank_loss_row['bank_ID']
        
        # Adjust the lookup to include 'Bank_ID'
        uninsured_deposit_value = uninsured_lookup.get((bank_name, bank_id), 0)
        
        # Calculate 'MM Asset' as the sum of 'total_loss' and 'gross_asset' (as defined in the paper)
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
    results_df = pd.DataFrame(results).sort_values(by=['bank_name', 'bank_ID'])
    
    return results_df

def insured_deposit_coverage_ratio(insured_deposit, uninsured_deposit, bank_losses):
    """
    Calculate the insured deposit coverage ratio for each bank based on the provided data.

    Parameters:
    insured_deposit (DataFrame): DataFrame containing insured deposit data
    uninsured_deposit (DataFrame): DataFrame containing uninsured deposit data
    bank_losses (DataFrame): DataFrame containing bank losses data

    Returns:
    DataFrame: A DataFrame containing the calculated insured deposit coverage ratio for each bank
    """
    # Initialize an empty list to store the results
    results = []
    
    # Create dictionaries from insured and uninsured deposits for quick lookup
    insured_lookup = insured_deposit.set_index(['bank_name', 'bank_ID'])['insured_deposit'].to_dict()
    uninsured_lookup = uninsured_deposit.set_index(['bank_name', 'bank_ID'])['uninsured_deposit'].to_dict()
    
    # Iterate over each row in bank_losses DataFrame
    for index, bank_loss_row in bank_losses.iterrows():
        bank_name = bank_loss_row['bank_name']
        bank_id = bank_loss_row['bank_ID']
        
        # Retrieve insured and uninsured deposit values
        insured_deposit_value = insured_lookup.get((bank_name, bank_id), 0)
        uninsured_deposit_value = uninsured_lookup.get((bank_name, bank_id), 0)
        
        # Calculate mark-to-market asset value as the sum of 'total_asset' minus 'total_loss'
        mark_to_market_asset_value = bank_loss_row['gross_asset'] + bank_loss_row['total_loss']
        
        # Calculate the insured deposit coverage ratio
        if insured_deposit_value > 0:  # Prevent division by zero
            uninsured_deposit_mm_asset_ratio = uninsured_deposit_value / mark_to_market_asset_value
            coverage_ratio = (mark_to_market_asset_value - uninsured_deposit_value - insured_deposit_value) / insured_deposit_value
        
        # Append the result
        results.append({
            'bank_name': bank_name,
            'bank_ID': bank_id,
            'total_loss': bank_loss_row['total_loss'], 
            'total_asset': bank_loss_row['gross_asset'],
            'mm_asset': mark_to_market_asset_value,
            'insured_deposit': insured_deposit_value,
            'uninsured_deposit': uninsured_deposit_value,
            'Uninsured_Deposit_MM_Asset': uninsured_deposit_mm_asset_ratio,
            'insured_deposit_coverage_ratio': coverage_ratio
        })
    
    # Convert results list to DataFrame
    results_df = pd.DataFrame(results)
    
    return results_df