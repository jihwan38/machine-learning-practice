# AWS RDS (PostGIS) 구축 및 세팅 가이드라인

본 프로젝트는 인프라 유연성과 마이크로서비스 구조 전환을 위해 데이터베이스를 도커 컴포즈 내 로컬 컨테이너에서 **AWS RDS**로 완전 분리하는 아키텍처를 채택했습니다.

이 문서는 추후 백엔드/인프라 담당자가 AWS RDS를 구축할 때 필수적으로 적용해야 하는 세팅 정보를 담고 있습니다.

## 1. RDS 인스턴스 기본 설정
* **데이터베이스 엔진:** PostgreSQL (최소 버전 14 이상 권장)
* **인스턴스 스펙:** `db.t3.micro` 이상 (공간 쿼리 메모리 소모를 고려해 여유가 있다면 `t3.medium` 권장)
* **네트워크 및 보안:** 
  - VPC 보안 그룹(Security Group)에서 인바운드 규칙에 **5432 포트**를 개방해야 합니다.
  - 외부 관리 툴(DBeaver, QGIS) 접속이 필요하다면 퍼블릭 액세스를 '허용'하되, 지정된 개발자 IP만 접근하도록 통제하는 것이 안전합니다.

## 2. PostGIS 확장 플러그인 활성화 (필수 ⭐)
AWS RDS는 기본적으로 공간 데이터 처리 모듈이 내장되어 있지만, 직접 수동으로 활성화하는 쿼리를 실행해야 합니다.
RDS가 생성되면 관리자(postgres 계정)로 최초 접속한 뒤, 아래 쿼리를 반드시 실행하세요.

```sql
-- 공간 데이터 및 지리 정보 처리를 위한 핵심 확장팩
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

## 3. 파이프라인 연동 환경변수 (.env)
RDS 구축이 완료되면, RDS 관리 콘솔에서 **엔드포인트(Endpoint) 주소**를 복사한 뒤, `ml-pipeline/.env` 파일의 연결 URI를 교체합니다.

```env
# 구성: postgresql://[사용자명]:[비밀번호]@[RDS엔드포인트주소]:5432/[DB명]
DATABASE_URL=postgresql://root:MySecretPassword123!@geoai-prod-db.cx...ap-northeast-2.rds.amazonaws.com:5432/geoai
```

## 4. 메인 서비스(동그라미온 등) DB 마이그레이션
쓰레기 무단투기 제보 원천 데이터(Ground Truth)를 수집하는 백엔드 서버의 DB 주소도 AWS RDS로 변경합니다.
이렇게 하면 실제 서비스에서 적재되는 최신 제보 데이터를 ML 파이프라인(Phase 0)이 실시간으로 긁어와 학습할 수 있게 됩니다.
