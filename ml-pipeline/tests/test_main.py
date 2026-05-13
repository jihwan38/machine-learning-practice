import pytest
from typer.testing import CliRunner
import geopandas as gpd
from shapely.geometry import Point

from main import app

runner = CliRunner()

@pytest.fixture
def dummy_result_gdf():
    """가짜 추론 결과 데이터"""
    return gpd.GeoDataFrame({
        'grid_id': [0, 1],
        'trash_score': [0.1, 0.9]
    }, geometry=[Point(0,0), Point(1,1)], crs="EPSG:5179")

def test_infer_hotspot_without_push(mocker, dummy_result_gdf):
    """
    --push 옵션이 없을 때: 
    로컬에 파일만 저장하고 DB 엔진(sqlalchemy)이 절대 호출되지 않아야 합니다.
    """
    mock_predictor_class = mocker.patch('main.HotspotPredictor')
    mock_predictor_instance = mock_predictor_class.return_value
    mock_predictor_instance.predict.return_value = dummy_result_gdf
    
    mocker.patch('geopandas.GeoDataFrame.to_file')
    mock_push = mocker.patch.object(mock_predictor_instance, 'push_to_db')

    result = runner.invoke(app, [
        "infer-hotspot", 
        "--train-region", "Test", 
        "--target-region", "Test"
    ])
    
    assert result.exit_code == 0
    assert "로컬 백업 저장 완료" in result.stdout
    assert "PostGIS DB 적재" not in result.stdout
    mock_push.assert_not_called()

def test_infer_hotspot_with_push(mocker, monkeypatch, dummy_result_gdf):
    """
    --push 옵션이 있을 때: 
    predictor.push_to_db 메서드가 정확하게 호출되어야 합니다.
    """
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    
    mock_predictor_class = mocker.patch('main.HotspotPredictor')
    mock_predictor_instance = mock_predictor_class.return_value
    mock_predictor_instance.predict.return_value = dummy_result_gdf
    
    mocker.patch('geopandas.GeoDataFrame.to_file')
    mock_push = mocker.patch.object(mock_predictor_instance, 'push_to_db')

    result = runner.invoke(app, [
        "infer-hotspot", 
        "--train-region", "Test", 
        "--target-region", "Test",
        "--push"
    ])
    
    assert result.exit_code == 0
    
    mock_push.assert_called_once_with(dummy_result_gdf, "sqlite:///:memory:")
