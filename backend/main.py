#main.py
from pydantic import BaseModel
from langchain.schema import HumanMessage, AIMessage 
from dotenv import load_dotenv

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from typing import List, Optional
from io import BytesIO
from zipfile import ZipFile

# MySQL 데이터베이스 설정 및 모델 가져오기
# from database import SessionLocal, Story, StoryCut

from database.models import Story, User

# 추가적인 모듈 가져오기
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

# 요청 모델 정의
class ChatRequest(BaseModel):
    sex: str
    message: str
    session_id: str

class StoryCutResponse(BaseModel):
    id: int
    text: Optional[str]  # Optional 처리
    description: Optional[str]
    image_prompt: Optional[str]
    image_path: Optional[str]

    class Config:
        from_attributes = True  # SQLAlchemy 객체 지원


class StoryResponse(BaseModel):
    session_id: str
    title: str
    story_text: Optional[str]
    recommendations: int
    views: int
    user_id: str
    cuts: List[StoryCutResponse]

    class Config:
        from_attributes = True

# API 엔드포인트 정의

# 대화 생성
@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        response = multi_turn_chat(request.sex, request.message, request.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# 대화 기록 조회
@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    chat_history = await store[session_id].aget_messages()
    history = [
        {
            "role": "user" if isinstance(msg, HumanMessage) else "ai",
            "content": msg.content
        }
        for msg in chat_history
    ]
    return {"session_id": session_id, "history": history}

# 이야기 생성 및 저장
@app.get("/story/{session_id}")
async def get_story(session_id: str, db: Session = Depends(get_db)):
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    chat_history = await store[session_id].aget_messages()
    story = "\n".join([msg.content for msg in chat_history if isinstance(msg, (HumanMessage, AIMessage))])
    
    try:
        final_story = story_chain.invoke({"story": story})
        story_entry = Story(session_id=session_id, story_text=final_story)
        db.add(story_entry)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")
    
    return {"session_id": session_id, "story": final_story}

# import redis

# # Redis 설정
# redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# @app.get("/story_view/{session_id}")
# async def get_story(session_id: str, db: Session = Depends(get_db)):
#     story = db.query(Story).filter(Story.session_id == session_id).first()
#     if not story:
#         raise HTTPException(status_code=404, detail="Story not found")
    
#     # Redis에서 조회수 증가
#     redis_key = f"story:{session_id}:views"
#     redis_client.incr(redis_key)

#     # 조회수 반환
#     views = int(redis_client.get(redis_key))

#     return {
#         "session_id": story.session_id,
#         "title": story.title,
#         "story_text": story.story_text,
#         "recommendations": story.recommendations,
#         "views": views,
#         "user": {
#             "user_id": story.user.user_id,
#             "name": story.user.name,
#             "age_group": story.user.age_group,
#         },
#         "cuts": [
#             {
#                 "id": cut.id,
#                 "description": cut.description,
#                 "image_prompt": cut.image_prompt,
#                 "image_path": cut.image_path,
#             }
#             for cut in story.cuts
#         ]
#     }

# @app.delete("/story_view/{session_id}")
# async def delete_story(session_id: str, db: Session = Depends(get_db)):
#     story = db.query(Story).filter(Story.session_id == session_id).first()
#     if not story:
#         raise HTTPException(status_code=404, detail="Story not found")
    
#     # 스토리 삭제
#     db.delete(story)
#     db.commit()  # 관련된 StoryCut도 자동 삭제
    
#     return {"message": f"Story with session_id {session_id} and its cuts were deleted."}

# # API: 모든 스토리 데이터 반환
# @app.get("/api/stories", response_model=List[StoryResponse])
# async def get_stories(db: Session = Depends(get_db)):
#     stories = db.query(Story).all()
#     # for story in stories:
#     #     print(f"Session ID: {story.session_id}, Title: {story.title}, Views: {story.views}")
#     return stories
# @app.get("/api/stories", response_model=List[StoryResponse])
# async def get_stories(db: Session = Depends(get_db)):
#     stories = db.query(Story).all()
#     for story in stories:
#         print(f"Session ID: {story.session_id}")
#         print(f"Title: {getattr(story, 'title', 'Attribute Missing')}")
#         print(f"Views: {getattr(story, 'views', 'Attribute Missing')}")
#     return stories

from sqlalchemy import text

@app.get("/api/stories")
async def get_stories_with_user_name(db: Session = Depends(get_db)):
    try:
        # SQL 쿼리를 작성하여 stories와 users를 조인
        query = text("""
        SELECT 
            s.session_id, s.title, s.story_text, s.recommendations, s.views, 
            u.name AS author,  -- 사용자 이름을 가져오기 위해 users.name 추가
            sc.id AS cut_id, sc.text AS cut_text, sc.description AS cut_description,
            sc.image_prompt, sc.image_path
        FROM stories s
        LEFT JOIN users u ON s.user_id = u.user_id  -- stories와 users 테이블 연결
        LEFT JOIN story_cuts sc ON s.session_id = sc.story_id
        """)
        result = db.execute(query.execution_options(stream_results=True))

        # 결과를 JSON 형태로 변환
        stories = {}
        for row in result.mappings():  # 딕셔너리 형태로 반환
            session_id = row["session_id"]
            if session_id not in stories:
                stories[session_id] = {
                    "session_id": session_id,
                    "title": row["title"],
                    "story_text": row["story_text"],
                    "recommendations": row["recommendations"],
                    "views": row["views"],
                    "author": row["author"],  # 사용자 이름 추가
                    "cuts": []
                }
            if row["cut_id"]:
                stories[session_id]["cuts"].append({
                    "id": row["cut_id"],
                    "text": row["cut_text"],
                    "description": row["cut_description"],
                    "image_prompt": row["image_prompt"],
                    "image_path": row["image_path"]
                })

        return list(stories.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API: 특정 스토리 삭제
@app.delete("/api/stories/{session_id}")
async def delete_story(session_id: str, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.session_id == session_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    db.delete(story)
    db.commit()
    return {"message": f"Story with session_id {session_id} has been deleted."}

# 이미지 생성
@app.get("/generate-image/{session_id}")
async def generate_image_from_story(session_id: str, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.session_id == session_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Session ID not found")

    img = generate_image(story=story.story_text)
    img_byte_array = BytesIO()
    img.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/png")

import os

# 이미지 저장 경로
IMAGE_STORAGE_PATH = "./static/"

# 이미지 저장 코드
@app.get("/generate-images/{session_id}")
async def generate_images_from_story(session_id: str, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.session_id == session_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Session ID not found")

    descriptions = story_to_img_chain.invoke({"story": story.story_text}).split('\n\n')
    zip_io = BytesIO()
    with ZipFile(zip_io, "w") as zip_file:
        for idx, description in enumerate(descriptions):
            prompt = description_to_prompt_chain.invoke({'description': description})
            img = generate_image(story=prompt)

            # 이미지 저장 경로 생성
            session_path = os.path.join(IMAGE_STORAGE_PATH, session_id)
            os.makedirs(session_path, exist_ok=True)  # 경로가 없으면 생성

            # 이미지 저장
            img_filename = f"{idx+1}.png"
            img_filepath = os.path.join(session_path, img_filename)
            img.save(img_filepath)

            # DB에 경로 저장
            story_cut = StoryCut(
                story_id=story.session_id,
                description=description,
                image_prompt=prompt,
                image_path=img_filepath
            )
            db.add(story_cut)
            zip_file.write(img_filepath, os.path.join(session_id, img_filename))

        db.commit()

    zip_io.seek(0)
    return StreamingResponse(zip_io, media_type="application/zip", headers={"Content-Disposition": "attachment;filename=images.zip"})
