# GeoAI Plogging ML Pipeline & Architecture

본 저장소는 공간 데이터(OSM, POI)와 쓰레기 무단투기 정답지(Ground Truth)를 활용하여, 지역 전체의 쓰레기 핫스팟(투기 위험도)을 예측하고 시각화하는 머신러닝 파이프라인(PU-Learning 기반)입니다.

이 프로젝트는 동구라미 API 등에서 수집한 라벨링 데이터를 바탕으로 작은 지역(예: 동구)에서 모델을 학습시키고, 라벨이 없는 넓은 지역(예: 광주 전체)으로 핫스팟 지도를 확장하는 **공간 전이 학습(Spatial Transfer Learning)**을 지원합니다.

## ⚙️ 1. 환경 설정 (`config.yaml`)

파이프라인을 실행하기 전, `ml-pipeline/config.yaml` 파일에서 대상 지역과 마스킹 설정을 확인해야 합니다.

```yaml
spatial:
  target_region: "Dong-gu, Gwangju, South Korea"  # 기본 타겟(학습) 지역 설정
  grid_size_meters: 10                            # 공간 격자의 해상도 (기본 10m)
  buffer_size_meters: 10                          # 도로 중심선 기준 마스킹 버퍼 반경 (기본 10m)
```
* **팁:** 모델 학습은 `target_region`에 맞춰 진행되지만, 이후 추론 단계 CLI 명령어에서 옵션을 통해 타겟 지역을 동적으로 바꿀 수 있습니다.

---

## 🚀 2. 로컬 실행 및 도커 배포

### 🔹 환경변수 세팅 (.env)
가장 먼저 `ml-pipeline/.env` 파일을 만들고 DB 주소를 입력합니다. (없을 경우 로컬 템플릿 사용)
```env
DATABASE_URL=postgresql://[아이디]:[비밀번호]@[호스트주소]:5432/[DB명]
```

### 🔹 Docker Compose를 이용한 실행 (로컬 실험 및 배포)
서버 배포 시 코드를 고칠 필요 없이 도커 명령어 한 줄로 완벽히 격리된 환경에서 실행이 가능합니다. 특히 다른 개발자의 컴퓨터에서도 환경 세팅 없이 바로 파이프라인을 돌려볼 수 있습니다.

**기본 도움말 확인:**
```bash
docker compose run --rm ml-pipeline uv run main.py --help
```

**실제 파이프라인 명령어 도커로 실행하기 (예시):**
도커 환경에서 파이프라인의 각 단계를 실행하려면 `docker compose run --rm ml-pipeline` 뒤에 기존 로컬 명령어를 그대로 붙여주면 됩니다.
```bash
# 데이터 수집
docker compose run --rm ml-pipeline uv run main.py fetch-raw-data

# 그리드 생성
docker compose run --rm ml-pipeline uv run main.py add-grid --region "Dong-gu, Gwangju, South Korea"

# 모델 학습
docker compose run --rm ml-pipeline uv run main.py train-model --region "Dong-gu, Gwangju, South Korea"
```
*(결과물인 `.pkl` 모델 파일이나 `.gpkg` 데이터는 도커 볼륨 마운트 설정에 의해 호스트 컴퓨터의 `ml-pipeline/data/` 폴더에 안전하게 영구 저장됩니다!)*

---

## 🗺️ 3. CLI 파이프라인 시나리오 (공간 전이 학습)

아래는 **"광주 동구(Dong-gu)에서 배운 인공지능을 이용해 광주 전체(Gwangju)의 쓰레기 지도를 그리는"** 전체 파이프라인 시나리오입니다. (로컬 실행 기준)

### [Phase 0] 정답 데이터 수집 (ETL)
외부 API(동구라미 등)에서 최신 쓰레기 신고 데이터를 가져와 PostGIS DB에 적재합니다.
```bash
uv run main.py fetch-raw-data
```

### [Phase 1~3] 동구(학습 지역) 도화지 및 피처 준비
동구 지역의 10m 격자를 만들고, 상권(POI) 피처를 계산합니다.
```bash
uv run main.py add-grid --region "Dong-gu, Gwangju, South Korea"
uv run main.py add-features --region "Dong-gu, Gwangju, South Korea"
```

### [Phase 4~5] 동구 기반 모델 학습 (Training)
DB에서 정답지(is_trash)를 불러와 동구의 격자 피처와 결합한 후, PU-XGBoost 모델을 학습시킵니다.
```bash
uv run main.py make-dataset --region "Dong-gu, Gwangju, South Korea"
uv run main.py train-model --region "Dong-gu, Gwangju, South Korea"
```
*(성공 시 `data/models/` 폴더에 `.pkl` 파일이 저장됩니다.)*

### [Phase 6] 광주 전체(타겟 지역) 도화지 및 피처 준비
이제 추론을 위해 광주 전체 크기의 도화지를 깔고 피처를 붙입니다.
```bash
uv run main.py add-grid --region "Gwangju, South Korea"
uv run main.py add-features --region "Gwangju, South Korea"
```

### [Phase 7] 핫스팟 추론 및 시각화 (Inference & Mapping)
동구에서 배운 모델(`--train-region`)을 가져와서 광주 전체(`--target-region`)에 대해 추론(trash_score)하고 고해상도 이미지를 렌더링합니다!
```bash
uv run main.py infer-hotspot \
  --train-region "Dong-gu, Gwangju, South Korea" \
  --target-region "Gwangju, South Korea"

uv run main.py visualize-hotspot --target-region "Gwangju, South Korea"
```
*(최종 결과물인 `result_hotspot_...gpkg` 파일과 히트맵 `.png` 이미지가 `data/processed/`에 안전하게 저장됩니다.)*
