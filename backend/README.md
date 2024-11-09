# Docker 이미지 빌드
docker build -t fastapi-langchain-app .

# Docker 컨테이너 실행
docker run -d -p 8000:8000 --env-file .env fastapi-langchain-app

------
# Docker Compose를 사용할 경우
docker-compose up -d

---
## 2024.11.09 Update
[x] gemini backend : `app.py`
[x] code refactoring

## 추가 진행사항 (~11.20)
[] 이미지 생성 api 연결
[] prompt engineering
