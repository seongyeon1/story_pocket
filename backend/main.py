from pydantic import BaseModel
from langchain.schema import HumanMessage, AIMessage 
from dotenv import load_dotenv

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from typing import List
from io import BytesIO
from zipfile import ZipFile

# MySQL 데이터베이스 설정 및 모델 가져오기
# from database import SessionLocal, Story, StoryCut

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

class StoryResponse(BaseModel):
    session_id: str
    story_text: str

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

# 이야기 조회
@app.get("/stories", response_model=List[StoryResponse])
async def get_all_stories(db: Session = Depends(get_db)):
    stories = db.query(Story).all()
    return stories

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

# # 여러 이미지 생성
# @app.get("/generate-images/{session_id}")
# async def generate_images_from_story(session_id: str, db: Session = Depends(get_db)):
#     story = db.query(Story).filter(Story.session_id == session_id).first()
#     if not story:
#         raise HTTPException(status_code=404, detail="Session ID not found")

#     descriptions = story_to_img_chain.invoke({"story": story.story_text}).split('\n')
#     zip_io = BytesIO()
#     with ZipFile(zip_io, "w") as zip_file:
#         for idx, description in enumerate(descriptions):
#             prompt = description_to_prompt_chain.invoke({'description': description})
#             img = generate_image(story=prompt)
#             img_byte_array = BytesIO()
#             img.save(img_byte_array, format="PNG")
#             img_byte_array.seek(0)

#             story_cut = StoryCut(
#                 story_id=story.session_id,
#                 description=description,
#                 image_prompt=prompt,
#                 image_data=img_byte_array.getvalue()
#             )
#             db.add(story_cut)
#             zip_file.writestr(f"image_{idx+1}.png", img_byte_array.getvalue())

#         db.commit()

#     zip_io.seek(0)
#     return StreamingResponse(zip_io, media_type="application/zip", headers={"Content-Disposition": "attachment;filename=images.zip"})


# import os

# class StoryCut(Base):
#     __tablename__ = "story_cuts"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     story_id = Column(String(255), ForeignKey("stories.session_id"), nullable=False)
#     description = Column(Text)
#     image_prompt = Column(Text)
#     image_path = Column(String(512))  # 이미지 파일 경로 저장

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