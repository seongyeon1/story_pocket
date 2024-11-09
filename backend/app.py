from pydantic import BaseModel
from langchain.schema import HumanMessage, AIMessage 
from dotenv import load_dotenv

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from io import BytesIO

from chat import *
from story import *
from img import *

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

# 데이터베이스 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI 요청 모델 정의
class ChatRequest(BaseModel):
    sex: str
    message: str
    session_id: str


# Story 데이터 모델을 위한 Pydantic 모델 정의
class StoryResponse(BaseModel):
    session_id: str
    story_text: str

    class Config:
        from_attributes = True

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

# 전체 대화 기록을 조회하고 이야기로 변환하여 데이터베이스에 저장하는 API 엔드포인트 정의
@app.get("/story/{session_id}")
async def get_story(session_id: str, db: Session = Depends(get_db)):
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    chat_history = await store[session_id].aget_messages()
    story = "\n".join([msg.content for msg in chat_history if isinstance(msg, (HumanMessage, AIMessage))])
    
    try:
        final_story = story_chain.invoke({"story": story})
        
        # 데이터베이스에 이야기 저장
        story_entry = Story(session_id=session_id, story_text=final_story)
        db.add(story_entry)
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")
    
    return {"session_id": session_id, "story": final_story}

# 모든 이야기 조회 API 엔드포인트 정의
@app.get("/stories", response_model=List[StoryResponse])
async def get_all_stories(db: Session = Depends(get_db)):
    stories = db.query(Story).all()
    return stories

# 이미지 생성 API 엔드포인트 정의
@app.get("/generate-image/{session_id}")
async def generate_image_from_story(session_id: str, db: Session = Depends(get_db)):
    # DB에서 해당 session_id의 story_text 조회
    story = db.query(Story).filter(Story.session_id == session_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Session ID not found")

    # story_text를 기반으로 이미지 생성
    img = generate_image(story=story.story_text)

    # 이미지 데이터를 바이트 스트림으로 변환하여 반환
    img_byte_array = BytesIO()
    img.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    
    return StreamingResponse(img_byte_array, media_type="image/png")



# # 데이터베이스 연결 설정
# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()