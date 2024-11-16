# Docker 이미지 빌드
docker build -t fastapi-langchain-app .

# Docker 컨테이너 실행
docker run -d -p 8000:8000 --env-file .env fastapi-langchain-app

------
# Docker Compose를 사용할 경우
docker-compose up -d

---
## 2024.11.09 Update
- [x] gemini backend : `app.py`
- [x] code refactoring

## 추가 진행사항 (~11.20)
- [ ] 이미지 생성 api 연결
- [ ] prompt engineering

## API 명세
API 명세서

기본 URL

	•	http://localhost:8000

1. /chat/

	•	설명: 사용자가 보내는 메시지에 대한 AI의 응답을 생성합니다.
	•	HTTP 메서드: POST
	•	Request Body: ChatRequest
	•	sex: str - 사용자의 성별
	•	message: str - 사용자가 보낸 메시지
	•	session_id: str - 대화 세션 ID
	•	응답:
	•	200 OK
	•	response: str - AI의 응답 메시지
	•	500 Internal Server Error: 서버 내부 에러 발생 시

2. /history/{session_id}

	•	설명: 특정 세션 ID에 대한 대화 기록을 조회합니다.
	•	HTTP 메서드: GET
	•	경로 매개변수:
	•	session_id: str - 대화 세션 ID
	•	응답:
	•	200 OK
	•	session_id: str - 세션 ID
	•	history: List[dict]
	•	role: str - 메시지의 발신자 (user 또는 ai)
	•	content: str - 메시지 내용
	•	404 Not Found: 유효하지 않은 세션 ID인 경우
	•	500 Internal Server Error: 서버 내부 에러 발생 시

3. /story/{session_id}

	•	설명: 특정 세션 ID에 대한 대화 기록을 가져와 이야기를 생성하고 데이터베이스에 저장합니다.
	•	HTTP 메서드: GET
	•	경로 매개변수:
	•	session_id: str - 대화 세션 ID
	•	응답:
	•	200 OK
	•	session_id: str - 세션 ID
	•	story: str - 생성된 이야기 텍스트
	•	404 Not Found: 유효하지 않은 세션 ID인 경우
	•	500 Internal Server Error: 이야기 생성 실패 또는 서버 내부 에러 발생 시

4. /stories

	•	설명: 데이터베이스에 저장된 모든 이야기를 조회합니다.
	•	HTTP 메서드: GET
	•	응답:
	•	200 OK
	•	List[StoryResponse]
	•	session_id: str - 세션 ID
	•	story_text: str - 이야기 텍스트
	•	500 Internal Server Error: 서버 내부 에러 발생 시

5. /generate-image/{session_id}

	•	설명: 특정 세션 ID의 이야기를 기반으로 이미지를 생성하고 반환합니다.
	•	HTTP 메서드: GET
	•	경로 매개변수:
	•	session_id: str - 이야기 세션 ID
	•	응답:
	•	200 OK
	•	이미지 파일 (image/png 형식)
	•	404 Not Found: 유효하지 않은 세션 ID인 경우
	•	500 Internal Server Error: 이미지 생성 실패 또는 서버 내부 에러 발생 시

6. /generate-images/{session_id}

	•	설명: 특정 세션 ID의 이야기를 기반으로 여러 이미지를 생성하여 ZIP 파일로 반환합니다.
	•	HTTP 메서드: GET
	•	경로 매개변수:
	•	session_id: str - 이야기 세션 ID
	•	응답:
	•	200 OK
	•	ZIP 파일 (application/zip 형식)
	•	각 이미지 파일 이름 형식: image_1.png, image_2.png, …
	•	404 Not Found: 유효하지 않은 세션 ID인 경우
	•	500 Internal Server Error: 이미지 생성 실패 또는 서버 내부 에러 발생 시

요청 예시

POST /chat/

{
  "sex": "female",
  "message": "안녕하세요",
  "session_id": "12345"
}

GET /history/12345

{
  "session_id": "12345",
  "history": [
    {"role": "user", "content": "안녕하세요"},
    {"role": "ai", "content": "안녕하세요! 어떻게 도와드릴까요?"}
  ]
}

GET /story/12345

{
  "session_id": "12345",
  "story": "사용자와 AI의 대화 내용이 요약된 이야기입니다."
}

GET /stories

[
  {
    "session_id": "12345",
    "story_text": "사용자와 AI의 대화 내용이 요약된 이야기입니다."
  }
]

응답 예시

GET /generate-image/12345

	•	응답: 이미지 파일 (image/png 형식)

GET /generate-images/12345

	•	응답: ZIP 파일 (application/zip 형식), 이미지 포함

    