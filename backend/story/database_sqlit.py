#pip install sqlalchemy databases

from sqlalchemy import create_engine, Column, String, Text, Integer, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from databases import Database

# SQLite 데이터베이스 URL 설정
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 연결을 위한 Database 객체 생성
database = Database(DATABASE_URL)

# Story 모델 정의
class Story(Base):
    __tablename__ = "stories"
    session_id = Column(String, primary_key=True, index=True)
    story_text = Column(Text)
    recommendations = Column(Integer, default=0)
    user_id = Column(String, index=True)

    # StoryCut와 일대다 관계
    cuts = relationship("StoryCut", back_populates="story")

# StoryCut 모델 정의
class StoryCut(Base):
    __tablename__ = "story_cuts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(String, ForeignKey("stories.session_id"), nullable=False)
    description = Column(Text)  # 묘사 내용
    image_prompt = Column(Text)  # 이미지 프롬프트
    image_data = Column(LargeBinary)  # 이미지 데이터 (바이트)

    # Story와 연결
    story = relationship("Story", back_populates="cuts")


# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)