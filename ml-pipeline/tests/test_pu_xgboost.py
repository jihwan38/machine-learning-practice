import pytest
import numpy as np
import pandas as pd
from src.models.pu_xgboost import PUBaggingXGBoost

def test_pu_xgboost_mutable_default():
    """정상 및 엣지 케이스: 가변 객체(Dict) 기본 인자 오염 방어 테스트"""
    model1 = PUBaggingXGBoost(n_estimators=2)
    model2 = PUBaggingXGBoost(n_estimators=2)
    
    model1.base_params['max_depth'] = 999
    assert model2.base_params['max_depth'] != 999
    assert model2.base_params['max_depth'] == 6

def test_pu_xgboost_fit_dimension_mismatch():
    """예외 케이스: X와 y의 데이터 개수가 다를 때 ValueError 발생 확인"""
    model = PUBaggingXGBoost()
    X = pd.DataFrame(np.random.rand(100, 5), columns=['A', 'B', 'C', 'D', 'E'])

    y = np.ones(90)

    with pytest.raises(ValueError, match="데이터 개수 불일치"):
        model.fit(X, y)

def test_pu_xgboost_fit_normal_case():
    """정상 케이스: 일반적인 학습 및 predict_proba 정상 동작 확인"""
    model = PUBaggingXGBoost(n_estimators=3, random_state=42)
    X = pd.DataFrame(np.random.rand(100, 3), columns=['F1', 'F2', 'F3'])
    y = np.zeros(100)
    y[:10] = 1

    model.fit(X, y)
    
    assert len(model.models) == 3
    
    probas = model.predict_proba(X)
    assert probas.shape == (100,)
    assert np.all(probas >= 0.0) and np.all(probas <= 1.0)

def test_pu_xgboost_no_positive_samples():
    """예외 케이스: 핫스팟(1) 데이터가 단 하나도 없을 때 ValueError 발생 검증"""
    model = PUBaggingXGBoost()
    X = pd.DataFrame(np.random.rand(50, 3), columns=['A', 'B', 'C'])
    y = np.zeros(50)

    with pytest.raises(ValueError, match="단 하나도 존재하지 않아"):
        model.fit(X, y)
