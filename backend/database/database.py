from sqlalchemy import create_engine, Column, String, Integer, LargeBinary, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# MySQL 데이터베이스 URL 설정
user = 'root'
password = ''  # MySQL 비밀번호
host = 'localhost'
port = '3306'
database_name = 'storypocket'
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Story 모델 정의
class Story(Base):
    __tablename__ = "stories"
    session_id = Column(String(255), primary_key=True, index=True)  # VARCHAR(255)
    story_text = Column(Text(length=4294967295))  # LONGTEXT
    recommendations = Column(Integer, default=0)
    user_id = Column(String(255), index=True)  # VARCHAR(255)

    # StoryCut와 일대다 관계
    cuts = relationship("StoryCut", back_populates="story")

# StoryCut 모델 정의
class StoryCut(Base):
    __tablename__ = "story_cuts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(String(255), ForeignKey("stories.session_id"), nullable=False)  # VARCHAR(255)
    description = Column(Text)  # TEXT
    image_prompt = Column(Text)  # TEXT
    # image_data = Column(LargeBinary(length=4294967295))  # BLOB
    image_path = Column(String(512))  # 이미지 파일 경로 저장

    # Story와 연결
    story = relationship("Story", back_populates="cuts")

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)