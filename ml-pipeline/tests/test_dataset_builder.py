import pytest
import geopandas as gpd
from shapely.geometry import box, Point
from src.dataset_builder import DatasetBuilder

def test_label_spatial_join(mocker, monkeypatch, dummy_config, dummy_grid_gdf, tmp_path):
    """
    실제 DB 연동이나 파일 쓰기 없이, 라벨 데이터가 격자와 올바르게
    병합되고 쓰레기 카운트가 계산되는지 파이프라인의 종점(build)을 테스트합니다.
    """
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    
    hotspots = gpd.GeoDataFrame({
        'is_trash': [1, 1]
    }, geometry=[Point(5, 5), Point(6, 6)], crs='EPSG:5179')
    
    mocker.patch('src.utils.load_config', return_value=dummy_config)
    mocker.patch('src.dataset_builder.BaselineViewLoader.load_view', return_value=hotspots)
    mocker.patch('pathlib.Path.exists', return_value=True)
    mocker.patch('geopandas.read_file', return_value=dummy_grid_gdf)
    mocker.patch('sqlalchemy.create_engine')
    
    mocker.patch('geopandas.GeoDataFrame.to_file')
    
    builder = DatasetBuilder("Test Region", 10, 10)
    builder.build()
    
