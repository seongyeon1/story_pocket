# Python 베이스 이미지
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt requirements.txt

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]