# 1. 빌더 스테이지 (가벼운 Python 이미지를 기반으로 시작)
FROM python:3.12-slim-bookworm AS builder

# uv 공식 이미지에서 uv 실행 파일만 쏙 빼옵니다 (설치 시간 0초)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 파이썬 실행 속도 최적화 환경변수
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# lock 파일만 먼저 복사 (도커 레이어 캐싱을 극대화하기 위함)
COPY pyproject.toml uv.lock ./

# [핵심] 개발용 툴(pytest 등)을 제외하고, uv.lock에 적힌 그대로 초고속 설치
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 나머지 코드(.py 파일 등) 복사 및 최종 동기화
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# ---------------------------------------------------------
# 2. 런타임 스테이지 (실제 서버에서 돌아갈 초경량 컨테이너)
FROM python:3.12-slim-bookworm
WORKDIR /app

# 빌더 스테이지에서 세팅이 끝난 가상환경(.venv)만 가져옴
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# PATH 환경변수를 .venv로 고정하여 파이썬 명령어 인식
ENV PATH="/app/.venv/bin:$PATH"

# 도커 컨테이너가 켜질 때 기본으로 실행될 명령어 (원하는 커맨드로 덮어쓰기 가능)
CMD ["python", "main.py", "--help"]
