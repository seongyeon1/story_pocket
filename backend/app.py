from pydantic import BaseModel
from langchain.schema import HumanMessage, AIMessage 

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chat import *
from story import *

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# FastAPI 요청 모델 정의
class ChatRequest(BaseModel):
    sex: str
    message: str
    session_id: str

# API 엔드포인트 정의 (대화 생성)
@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        # multi_turn_chat 함수가 비동기가 아닌 경우 await 없이 호출
        response = multi_turn_chat(request.sex, request.message, request.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# 전체 대화 기록을 조회하는 API 엔드포인트 정의
@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    # 해당 session_id가 존재하지 않으면 에러 반환
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    # 대화 히스토리 가져오기
    chat_history = await store[session_id].aget_messages()
    
    # 메시지의 종류에 따라 역할(role)을 지정해 대화 기록 반환
    history = [
        {
            "role": "user" if isinstance(msg, HumanMessage) else "ai",
            "content": msg.content
        }
        for msg in chat_history
    ]
    
    return {"session_id": session_id, "history": history}

# 전체 대화 기록을 조회하고 이야기로 변환하는 API 엔드포인트 정의
@app.get("/story/{session_id}")
async def get_story(session_id: str):
    # 해당 session_id가 존재하지 않으면 에러 반환
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    # 대화 히스토리 가져오기
    chat_history = await store[session_id].aget_messages()
    
    # 대화 내용을 story 형식으로 변환
    story = "\n".join([msg.content for msg in chat_history if isinstance(msg, (HumanMessage, AIMessage))])
    
    # story를 템플릿을 이용해 할아버지의 이야기 형식으로 변환
    try:
        final_story = story_chain.invoke({"story": story})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")
    
    return {"session_id": session_id, "story": final_story}