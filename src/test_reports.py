import pandas as pd
import pytest
import load_assets

rcfd_data_1 = load_assets.load_wrds_reports('ddss0fpozaxonboe') #series 1 of rcfd
rcfd_data_2 = load_assets.load_wrds_reports('dycfrwcdm9puanhs') #series 2 of rcfd
rcon_data_1 = load_assets.load_wrds_reports('m3pzkcjsgvk26dwa') #series 1 of rcon
rcon_data_2 = load_assets.load_wrds_reports('hwv0m9qml6efztsi') #series 2 of rcon
rcfn_data = load_assets.load_wrds_reports('cipzs5x6g2axzlhe') #rcfn

def test_asset_cleaning():
    analysis_date = '03/31/2022'
    filtered_asset_level_0 = load_assets.clean_assets(rcfd_data_2,'RCFD2170',analysis_date)
    filtered_asset_level = load_assets.clean_assets(rcon_data_2,'RCON2170',analysis_date)
    df_asset = pd.concat([filtered_asset_level_0, filtered_asset_level])
    desired_shape = (4844, 4)
    total_assets = 23988517644.0

    assert isinstance(df_asset,pd.DataFrame)
    assert df_asset.shape == desired_shape
    assert df_asset.iloc[:,-1].sum() == total_assets

def test_loan_cleaning():
    analysis_date = '03/31/2022'
    rcon_cols = ['RCONA564', 'RCONA565', 'RCONA566', 'RCONA567', 'RCONA568', 'RCONA569']
    rcon_cols2 = ['RCONA570', 'RCONA571', 'RCONA572', 'RCONA573', 'RCONA574', 'RCONA575']
    rcfd_cols = ['RCFDA570', 'RCFDA571', 'RCFDA572', 'RCFDA573', 'RCFDA574', 'RCFDA575']

    df_loans_first_lien_domestic = load_assets.clean_loans(rcon_data_1,rcon_cols,analysis_date)
    df_loans_exc_first_lien = load_assets.clean_loans(rcfd_data_1,rcfd_cols,analysis_date)
    df_loans_exc_first_lien_domestic = load_assets.clean_loans(rcon_data_2,rcon_cols2,analysis_date)

    df_other_loan = pd.concat([df_loans_exc_first_lien_domestic, df_loans_exc_first_lien])

    desired_shape = (4844, 9)
    total_loans = 9070794634.0

    assert isinstance(df_loans_first_lien_domestic,pd.DataFrame)
    assert len(df_loans_first_lien_domestic) == desired_shape[0]
    assert df_other_loan.shape == desired_shape
    assert df_other_loan.iloc[:,-6:].sum().sum() == total_loans


