import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import box, Point

@pytest.fixture
def dummy_config():
    return {
        'spatial': {
            'base_crs': 'EPSG:4326',
            'projected_crs': 'EPSG:5179',
            'target_region': 'Test Region',
            'grid_size_meters': 10,
            'buffer_size_meters': 10
        },
        'data': {
            'paths': {
                'raw': 'data/raw',
                'processed': 'data/processed'
            }
        }
    }

@pytest.fixture
def dummy_grid_gdf():
    """2개의 10x10 격자 (x=0~10, x=10~20)"""
    polygons = [
        box(0, 0, 10, 10),
        box(10, 0, 20, 10)
    ]
    gdf = gpd.GeoDataFrame(geometry=polygons, crs='EPSG:5179')
    gdf['grid_id'] = ['0', '1']
    return gdf

@pytest.fixture
def dummy_poi_df():
    """가상의 POI 데이터 (좌표는 실제 테스트 시 교체하여 사용)"""
    return pd.DataFrame({
        '상권업종대분류명': ['음식', '소매', '관광/여가/오락', '음식'],
        '상권업종중분류명': ['한식', '종합소매점', '무도/유흥/가무', '주점'],
        '경도': [126.9, 126.91, 126.92, 126.93],
        '위도': [37.5, 37.51, 37.52, 37.53]
    })
