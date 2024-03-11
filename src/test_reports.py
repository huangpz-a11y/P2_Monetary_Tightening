import pandas as pd
import pytest
import load_assets

rcfd_data_1 = load_assets.load_wrds_reports('ddss0fpozaxonboe') #series 1 of rcfd
rcfd_data_2 = load_assets.load_wrds_reports('dycfrwcdm9puanhs') #series 2 of rcfd
rcon_data_1 = load_assets.load_wrds_reports('m3pzkcjsgvk26dwa') #series 1 of rcon
rcon_data_2 = load_assets.load_wrds_reports('hwv0m9qml6efztsi') #series 2 of rcon
rcfn_data = load_assets.load_wrds_reports('cipzs5x6g2axzlhe') #rcfn

analysis_date = '03/31/2022'
filtered_asset_level_0 = load_assets.clean_assets(rcfd_data_2,'RCFD2170',analysis_date)
filtered_asset_level = load_assets.clean_assets(rcon_data_2,'RCON2170',analysis_date)

rcon_cols = ['RCONA564', 'RCONA565', 'RCONA566', 'RCONA567', 'RCONA568', 'RCONA569']
rcon_cols2 = ['RCONA570', 'RCONA571', 'RCONA572', 'RCONA573', 'RCONA574', 'RCONA575']
rcfd_cols = ['RCFDA570', 'RCFDA571', 'RCFDA572', 'RCFDA573', 'RCFDA574', 'RCFDA575']
df_loans_first_lien_domestic = load_assets.clean_loans(rcon_data_1,rcon_cols,analysis_date)
df_loans_exc_first_lien = load_assets.clean_loans(rcfd_data_1,rcfd_cols,analysis_date)
df_loans_exc_first_lien_domestic = load_assets.clean_loans(rcon_data_2,rcon_cols2,analysis_date)

rmbs_cols = ['RCFDA555', 'RCFDA556', 'RCFDA557', 'RCFDA558', 'RCFDA559', 'RCFDA560']
rmbs_dom_cols = ['RCONA555', 'RCONA556', 'RCONA557', 'RCONA558', 'RCONA559', 'RCONA560']
df_RMBS = load_assets.clean_loans(rcfd_data_1,rmbs_cols,analysis_date)
df_RMBS_dom = load_assets.clean_loans(rcon_data_1,rmbs_dom_cols,analysis_date)

non_RMBS_cols = ['RCFDA549', 'RCFDA550', 'RCFDA551', 'RCFDA552', 'RCFDA553', 'RCFDA554']
non_RMBS_dom_cols = ['RCONA549', 'RCONA550', 'RCONA551', 'RCONA552', 'RCONA553', 'RCONA554']
df_non_RMBS = load_assets.clean_loans(rcfd_data_2,non_RMBS_cols,analysis_date)
df_non_RMBS_dom = load_assets.clean_loans(rcon_data_2,non_RMBS_dom_cols,analysis_date)

df_asset = pd.concat([filtered_asset_level_0, filtered_asset_level])
df_other_loan = pd.concat([df_loans_exc_first_lien_domestic, df_loans_exc_first_lien])
df_RMBS_Final = pd.concat([df_RMBS_dom, df_RMBS])
df_treasury_and_others = pd.concat([df_non_RMBS_dom, df_non_RMBS])

def test_asset_cleaning():
    desired_shape = (4844, 4)
    total_assets = 23988517644.0

    assert isinstance(df_asset,pd.DataFrame)
    assert df_asset.shape == desired_shape
    assert df_asset.iloc[:,-1].sum() == total_assets

def test_loan_cleaning():  
    desired_shape = (4844, 9)
    total_loans = 9070794634.0
    expected_RMBS = 2352325983.0

    assert isinstance(df_loans_first_lien_domestic,pd.DataFrame)
    assert len(df_loans_first_lien_domestic) == desired_shape[0]
    assert df_other_loan.shape == desired_shape
    assert df_other_loan.iloc[:,-6:].sum().sum() == total_loans
    assert df_RMBS_Final.iloc[:,-6:].sum().sum() == expected_RMBS

def test_all_reports():
    total_assets_sum = 0

    for df in [df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan]:
        total = df.iloc[:,-6:].sum().sum()
        total_assets_sum += total
    
    expected = 16590518404.0

    assert total_assets_sum == expected

def test_all_reports_total_assets_non_negative():
    total_assets_sum = 0

    for df in [df_RMBS_Final, df_loans_first_lien_domestic, df_treasury_and_others, df_other_loan]:
        total = df.iloc[:,-6:].sum().sum()
        total_assets_sum += total

    assert total_assets_sum >= 0



