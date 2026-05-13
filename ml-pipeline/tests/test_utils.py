import pytest
import geopandas as gpd
from shapely.geometry import Point
from src.utils import get_safe_region_name, ensure_crs

def test_get_safe_region_name():
    """지역명 변환 유틸리티가 공백, 쉼표, 대문자를 올바르게 처리하는지 검증합니다."""
    assert get_safe_region_name("Dong-gu, Gwangju") == "dong-gu_gwangju"
    assert get_safe_region_name("Seoul, South Korea") == "seoul_south_korea"
    assert get_safe_region_name("   TEST,  ") == "test"

def test_ensure_crs():
    """ CRS 강제 변환 안전장치가 제대로 작동하는지 검증합니다."""
    gdf_no_crs = gpd.GeoDataFrame(geometry=[Point(0, 0)])
    with pytest.raises(ValueError, match="데이터 프레임에 CRS 정보가 없습니다"):
        ensure_crs(gdf_no_crs, "EPSG:5179")
        
    gdf_4326 = gpd.GeoDataFrame(geometry=[Point(126.9, 37.5), Point(126.91, 37.51)], crs="EPSG:4326")
    gdf_5179 = ensure_crs(gdf_4326, "EPSG:5179")
    assert gdf_5179.crs.to_string() == "EPSG:5179"
    
    gdf_same = ensure_crs(gdf_5179, "EPSG:5179")
    assert gdf_same is gdf_5179

