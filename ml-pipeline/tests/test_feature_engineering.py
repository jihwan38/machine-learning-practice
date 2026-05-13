import pytest
from src.feature_engineering import POIFeatureExtractor

def test_categorize_poi():
    """상권 분류 로직이 규칙에 맞게 5개 카테고리로 매핑하는지 검증합니다."""
    test_cases = [
        ({'상권업종대분류명': '음식', '상권업종중분류명': '주점'}, 'nightlife'),
        ({'상권업종대분류명': '음식', '상권업종중분류명': '비알코올'}, 'cafe'),
        ({'상권업종대분류명': '음식', '상권업종중분류명': '기타 간이'}, 'cafe'),
        ({'상권업종대분류명': '음식', '상권업종중분류명': '한식'}, 'food'),
        ({'상권업종대분류명': '소매', '상권업종중분류명': '종합소매점'}, 'retail'),
        ({'상권업종대분류명': '관광/여가/오락', '상권업종중분류명': '무도/유흥/가무'}, 'service'),
    ]
    
    for row, expected in test_cases:
        assert POIFeatureExtractor._categorize_poi(row) == expected

def test_poi_spatial_join(mocker, dummy_config, dummy_grid_gdf, dummy_poi_df, tmp_path):
    """실제 파일을 읽지 않고, 가짜 데이터(Fixture)를 주입(Mock)하여 버퍼 연산과 카운팅 로직을 검증합니다."""
    mocker.patch('pathlib.Path.exists', return_value=True)
    mocker.patch('pandas.read_csv', return_value=dummy_poi_df)
    
    extractor = POIFeatureExtractor(dummy_config, "Test Region", tmp_path)
    
    result_gdf = extractor.extract(dummy_grid_gdf)
    
    expected_columns = [
        'food_count_30m', 'food_count_50m', 'food_count_100m',
        'retail_count_30m', 'retail_count_50m', 'retail_count_100m',
        'nightlife_count_30m', 'nightlife_count_50m', 'nightlife_count_100m',
        'service_count_30m', 'service_count_50m', 'service_count_100m'
    ]
    
    for col in expected_columns:
        assert col in result_gdf.columns, f"{col} 피처가 생성되지 않았습니다."
        
    assert not result_gdf['food_count_30m'].isnull().any()
