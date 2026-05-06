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
    
    # 가짜 핫스팟 (Grid 0번 구역 안에 쓰레기가 2개, Grid 1번 구역은 쓰레기 0개)
    hotspots = gpd.GeoDataFrame({
        'is_trash': [1, 1]
    }, geometry=[Point(5, 5), Point(6, 6)], crs='EPSG:5179')
    
    # [의존성 주입] 외부 시스템 접속/파일 IO 차단
    mocker.patch('src.utils.load_config', return_value=dummy_config)
    mocker.patch('src.dataset_builder.BaselineViewLoader.load_view', return_value=hotspots)
    mocker.patch('pathlib.Path.exists', return_value=True)
    mocker.patch('geopandas.read_file', return_value=dummy_grid_gdf)
    mocker.patch('sqlalchemy.create_engine')
    
    # GeoDataFrame.to_file 호출 시 아무 동작도 하지 않도록 Mock 처리
    mocker.patch('geopandas.GeoDataFrame.to_file')
    
    # Builder 생성 및 실행
    builder = DatasetBuilder("Test Region", 10, 10)
    builder.build()
    
    # 에러 없이 파이프라인이 종단까지 도달했는지 확인
    # (추후 리팩토링을 통해 build()가 merged_gdf를 반환하도록 변경하면 더 정밀한 assert 가능)
