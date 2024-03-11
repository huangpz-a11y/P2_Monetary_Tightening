import pandas as pd
import pytest
import load_assets

rcfd_data_1 = load_assets.load_wrds_reports('ddss0fpozaxonboe') #series 1 of rcfd
rcfd_data_2 = load_assets.load_wrds_reports('dycfrwcdm9puanhs') #series 2 of rcfd
rcon_data_1 = load_assets.load_wrds_reports('m3pzkcjsgvk26dwa') #series 1 of rcon
rcon_data_2 = load_assets.load_wrds_reports('hwv0m9qml6efztsi') #series 2 of rcon
rcfn_data = load_assets.load_wrds_reports('cipzs5x6g2axzlhe') #rcfn

def test_cleaning():
    analysis_date = '03/31/2022'
    filtered_asset_level_0 = load_assets.clean_assets(rcfd_data_2,'RCFD2170',analysis_date)
    filtered_asset_level = load_assets.clean_assets(rcon_data_2,'RCON2170',analysis_date)
    df_asset = pd.concat([filtered_asset_level_0, filtered_asset_level])
    desired_shape = (4844, 4)
    total_assets = 23988517644.0

    assert isinstance(df_asset,pd.DataFrame)
    assert df_asset.shape == desired_shape
    assert df_asset.iloc[:,-1].sum() == total_assets

