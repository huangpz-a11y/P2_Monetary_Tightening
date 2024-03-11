import pandas as pd
import Calc_table_statistic as calcstat

def calculate_summary_statistics(df):
    """
    Calculates and returns summary statistics for the input DataFrame.

    The input DataFrame is expected to have columns corresponding to different types of financial metrics
    such as total losses, asset shares, uninsured deposit/MM asset ratios, and insured deposit coverage ratios.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the financial metrics for which to calculate summary statistics.

    Returns:
    - pd.DataFrame: Summary statistics including mean, median, standard deviation, skewness, and kurtosis for each column in the input DataFrame.
    """

    # Calculate mean - represents the average value, providing an insight into the central tendency of the data.
    mean = df.mean()

    # Calculate median - the middle value when the data is ordered, useful for understanding the central point of the data distribution, especially in skewed distributions.
    median = df.median()

    # Calculate standard deviation - measures the dispersion or variability of the data, indicating the typical distance of the data points from the mean.
    standard_deviation = df.std()

    # Calculate skewness - assesses the asymmetry of the distribution of data. Positive skew indicates a tail on the right side, negative skew a tail on the left. This is crucial for understanding the direction of risk exposure.
    skewness = df.skew()

    # Calculate kurtosis - measures the 'tailedness' of the distribution. High kurtosis indicates a distribution with heavy tails, suggesting a higher risk of outlier events.
    kurtosis = df.kurtosis()

    summary_df = pd.DataFrame({
        'Mean': mean,
        'Median': median,
        'Standard Deviation': standard_deviation,
        'Skewness': skewness,
        'Kurtosis': kurtosis
    })

    return summary_df

summary_statistics = calculate_summary_statistics(calcstat.bank_losses_assets)
print(summary_statistics)

