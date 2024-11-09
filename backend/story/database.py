#pip install sqlalchemy databases
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)