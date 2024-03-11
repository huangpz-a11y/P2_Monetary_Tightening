import pandas as pd
import pytest
import data_read


sp_1_3 = data_read.process_sp_data('S&P 1-3','sp 1-3')
sp_3_5 = data_read.process_sp_data('S&P 3-5','sp 3-5')
sp_7_10 = data_read.process_sp_data('S&P 7-10','sp 7-10')

def test_df_range():
    """
    Test the range of the dataframes for sp_1_3, sp_3_5, and sp_7_10
    """
    test_vals1 = [340.2, 332.77]
    test_vals2 = [488.75,461.71]
    test_vals3 = [680.3, 606.15]
    test_dates =['2022-01-03','2023-03-31']

    for i in range(2):
        assert sp_1_3[sp_1_3.index == test_dates[i]].iloc[0,0] == test_vals1[i]
        assert sp_3_5[sp_3_5.index == test_dates[i]].iloc[0,0] == test_vals2[i]
        assert sp_7_10[sp_7_10.index == test_dates[i]].iloc[0,0] == test_vals3[i]

def test_combined_df():
    """
    Test the combined dataframe for ishares, sp_1_3, sp_3_5, and sp_7_10, and other ETFs
    """
    ishares = data_read.load_df('ishares')
    df_ls = [ishares,sp_1_3,sp_3_5,sp_7_10]
    combined_df = data_read.combine_dfs(df_ls)

    # arbitrary date interval within the desired time range
    test_range = combined_df[combined_df.index >= '2022-07-01'].head()
    desired_size = (5, 8)
    test_string1 = test_range.to_string().replace(" ", "").replace("\n", "")
    
    test_string2 ='''
        iShares 0-1  iShares 1-3  iShares 7-10  iShares 10-20  iShares 20+  sp 1-3  sp 3-5  sp 7-10
        date                                                                                                   
        2022-07-01   101.980003    79.260551     98.588120     114.192192   109.723854  331.17  464.47   620.23
        2022-07-02   101.980003    79.260551     98.588120     114.192192   109.723854  331.17  464.47   620.23
        2022-07-03   101.980003    79.260551     98.588120     114.192192   109.723854  331.17  464.47   620.23
        2022-07-04   101.970001    79.260551     98.588120     114.192192   109.723854  331.17  464.47   620.23
        2022-07-05   101.959999    79.250984     98.951019     114.890854   110.585976  331.28  465.09   623.16

    '''

    test_string2 = test_string2.replace(" ", "").replace("\n", "")

    # assert test_string1[100:112] == test_string2[100:112] 
    assert test_range.shape == desired_size
    assert test_string1 == test_string2
