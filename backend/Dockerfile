# Python 3.12 베이스 이미지 사용
FROM python:3.12

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# FastAPI 앱 시작
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]