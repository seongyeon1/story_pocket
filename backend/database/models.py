#models.py
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date

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

# User 모델 정의
class User(Base):
    __tablename__ = "users"
    user_id = Column(String(255), primary_key=True, index=True)  # 사용자 ID
    name = Column(String(255), nullable=False)  # 이름
    password = Column(String(255), nullable=False)  # 비밀번호
    phone = Column(String(20), unique=True, nullable=False)  # 전화번호
    birth_date = Column(Date, nullable=False)  # 출생 연월일
    gender = Column(String(10), nullable=False)  # 성별
    join_date = Column(DateTime, default=datetime.utcnow)  # 가입일자

    # Story와 일대다 관계
    stories = relationship("Story", back_populates="user")

    # 연령대를 반환하는 함수
    @property
    def age_group(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return "Senior" if age >= 65 else "Adult"

# Story 모델 정의
class Story(Base):
    __tablename__ = "stories"
    session_id = Column(String(255), primary_key=True, index=True)
    # title = Column(String(255), nullable=False)  # 제목
    story_text = Column(Text(length=4294967295), nullable=True)  # 스토리 내용
    recommendations = Column(Integer, default=0, nullable=False)  # 추천 수
    views = Column(Integer, default=0, nullable=False)  # 조회수
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="stories")
    cuts = relationship("StoryCut", back_populates="story", cascade="all, delete-orphan")
# StoryCut 모델 정의
class StoryCut(Base):
    __tablename__ = "story_cuts"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 컷 ID
    story_id = Column(String(255), ForeignKey("stories.session_id"), nullable=False)  # 스토리 ID
    text = Column(String(512)) #동화
    description = Column(Text)  # 묘사 내용
    image_prompt = Column(Text)  # 이미지 프롬프트
    image_path = Column(String(512))  # 이미지 파일 경로

    # Story와 연결
    story = relationship("Story", back_populates="cuts")

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)