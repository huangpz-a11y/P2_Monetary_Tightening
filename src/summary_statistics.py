import pandas as pd
import Calc_table_statistic as calcstat


def calculate_summary_statistics_for_multiple_dfs(dfs_dict):
    """
    Calculates and returns summary statistics for multiple input DataFrames provided in a dictionary.
    
    Each input DataFrame in the dictionary is expected to have columns corresponding to different types of financial metrics.
    
    Parameters:
    - dfs_dict (dict): A dictionary where keys are descriptive names of the DataFrames and values are the DataFrames themselves.
    
    Returns:
    - dict: A dictionary where keys are the same descriptive names provided in the input, and values are DataFrames containing summary statistics for each input DataFrame.
    """
    
    summary_statistics_dict = {}
    
    for df_name, df in dfs_dict.items():
        mean = df.mean()
        median = df.median()
        standard_deviation = df.std()
        skewness = df.skew()
        kurtosis = df.kurtosis()
        
        summary_df = pd.DataFrame({
            'Mean': mean,
            'Median': median,
            'Standard Deviation': standard_deviation,
            'Skewness': skewness,
            'Kurtosis': kurtosis
        })
        
        summary_statistics_dict[df_name] = summary_df
    
    return summary_statistics_dict

# Example usage:
# Assuming we have multiple DataFrames: bank_losses_assets, uninsured_deposit_mm_asset, insured_deposit_coverage, each containing different financial metrics.
dfs_dict = {
    'Bank Losses & Assets': calcstat.bank_losses_assets,
    'Uninsured Deposit/MM Asset Ratios': calcstat.uninsured_deposit_mm_asset,
    'Insured Deposit Coverage Ratios': calcstat.insured_deposit_coverage
}
summary_statistics = calculate_summary_statistics_for_multiple_dfs(dfs_dict)

for df_name, summary_df in summary_statistics.items():
    print(f"Summary statistics for {df_name}:")
    print(summary_df)
    print("\n")






# def calculate_summary_statistics(df):
#     """
#     Calculates and returns summary statistics for the input DataFrame.

#     The input DataFrame is expected to have columns corresponding to different types of financial metrics
#     such as total losses, asset shares, uninsured deposit/MM asset ratios, and insured deposit coverage ratios.

#     Parameters:
#     - df (pd.DataFrame): DataFrame containing the financial metrics for which to calculate summary statistics.

#     Returns:
#     - pd.DataFrame: Summary statistics including mean, median, standard deviation, skewness, and kurtosis for each column in the input DataFrame.
#     """

#     # Calculate mean - represents the average value, providing an insight into the central tendency of the data.
#     mean = df.mean()

#     # Calculate median - the middle value when the data is ordered, useful for understanding the central point of the data distribution, especially in skewed distributions.
#     median = df.median()

#     # Calculate standard deviation - measures the dispersion or variability of the data, indicating the typical distance of the data points from the mean.
#     standard_deviation = df.std()

#     # Calculate skewness - assesses the asymmetry of the distribution of data. Positive skew indicates a tail on the right side, negative skew a tail on the left. This is crucial for understanding the direction of risk exposure.
#     skewness = df.skew()

#     # Calculate kurtosis - measures the 'tailedness' of the distribution. High kurtosis indicates a distribution with heavy tails, suggesting a higher risk of outlier events.
#     kurtosis = df.kurtosis()

#     summary_df = pd.DataFrame({
#         'Mean': mean,
#         'Median': median,
#         'Standard Deviation': standard_deviation,
#         'Skewness': skewness,
#         'Kurtosis': kurtosis
#     })

#     return summary_df

# summary_statistics = calculate_summary_statistics(calcstat.bank_losses_assets)
# print(summary_statistics)
