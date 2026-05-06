import pytest
import numpy as np
import pandas as pd
from src.models.pu_xgboost import PUBaggingXGBoost

def test_pu_xgboost_mutable_default():
    """정상 및 엣지 케이스: 가변 객체(Dict) 기본 인자 오염 방어 테스트"""
    # Python의 악명 높은 가변 객체(Mutable Default Argument) 버그가 잘 방어되었는지 테스트
    model1 = PUBaggingXGBoost(n_estimators=2)
    model2 = PUBaggingXGBoost(n_estimators=2)
    
    # model1의 설정값을 내부에서 임의로 수정해도 model2에 전염(?)되지 않아야 합니다.
    model1.base_params['max_depth'] = 999
    assert model2.base_params['max_depth'] != 999
    assert model2.base_params['max_depth'] == 6  # 기본값 유지

def test_pu_xgboost_fit_dimension_mismatch():
    """예외 케이스: X와 y의 데이터 개수가 다를 때 ValueError 발생 확인"""
    model = PUBaggingXGBoost()
    X = pd.DataFrame(np.random.rand(100, 5), columns=['A', 'B', 'C', 'D', 'E'])  # 100건의 데이터 (DataFrame 형식을 맞춰줌)
    y = np.ones(90)             # 90건의 정답지
    
    # 길이 불일치 시 명시적인 ValueError를 발생시켜 조기 종료되는지 검증
    with pytest.raises(ValueError, match="데이터 개수 불일치"):
        model.fit(X, y)

def test_pu_xgboost_fit_normal_case():
    """정상 케이스: 일반적인 학습 및 predict_proba 정상 동작 확인"""
    model = PUBaggingXGBoost(n_estimators=3, random_state=42)
    X = pd.DataFrame(np.random.rand(100, 3), columns=['F1', 'F2', 'F3'])
    y = np.zeros(100)
    y[:10] = 1 # 10개의 Positive(핫스팟), 90개의 Unlabeled
    
    model.fit(X, y)
    
    # 1. 지정한 수(3명)만큼 모델이 고용되었는지 확인
    assert len(model.models) == 3
    
    # 2. 예측 확률값이 0.0~1.0 범위를 잘 지키고 (100,) 1D 배열로 잘 나오는지 확인
    probas = model.predict_proba(X)
    assert probas.shape == (100,)
    assert np.all(probas >= 0.0) and np.all(probas <= 1.0)

def test_pu_xgboost_no_positive_samples():
    """예외 케이스: 핫스팟(1) 데이터가 단 하나도 없을 때 ValueError 발생 검증"""
    model = PUBaggingXGBoost()
    X = pd.DataFrame(np.random.rand(50, 3), columns=['A', 'B', 'C'])
    y = np.zeros(50)  # 전부 0(Unlabeled) 데이터만 존재함
    
    with pytest.raises(ValueError, match="단 하나도 존재하지 않아"):
        model.fit(X, y)
