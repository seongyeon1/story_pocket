from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from models import Base, User, Story, StoryCut, engine

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 세션 생성
db = Session(bind=engine)

# 더미 데이터 생성
def create_dummy_data():
    # 1. 사용자 생성
    users = [
        User(
            user_id="user001",
            name="홍길동",
            password="password123",
            phone="01012345678",
            birth_date=date.today() - timedelta(days=30 * 365),  # 30세
            gender="남성",
            join_date=datetime.utcnow()
        ),
        User(
            user_id="user002",
            name="김순자",
            password="password123",
            phone="01087654321",
            birth_date=date.today() - timedelta(days=70 * 365),  # 70세
            gender="여성",
            join_date=datetime.utcnow()
        ),
        User(
            user_id="user003",
            name="이영희",
            password="password123",
            phone="01056789012",
            birth_date=date.today() - timedelta(days=80 * 365),  # 80세
            gender="여성",
            join_date=datetime.utcnow()
        ),
    ]
    db.add_all(users)
    db.commit()

    # 2. 사용자 별로 다른 스토리 생성
    user_stories = {
        "user002": {
            "story_text": """
                저는 1950년대에 태어나 논밭 사이에 있는 작은 마을에서 자랐습니다. 
                매일 아침 학교까지 5리를 걸어가야 했는데, 길가에는 늘 새소리가 들렸죠.
                친구들과 도시락을 나눠 먹던 그때의 추억은 정말 소중합니다.
            """,
            "cuts": [
                {
                    "description": "새소리를 들으며 논밭 사이 길을 걷는 아이.",
                    "image_prompt": (
                        "Fairy tale style, a child walking along a dirt path surrounded by lush rice fields, "
                        "with birds chirping in the background under a clear blue sky."
                    ),
                    "image_path": "/images/story_user002_cut_1.png"
                },
                {
                    "description": "나무 아래 친구들과 도시락을 나눠 먹는 모습.",
                    "image_prompt": (
                        "Fairy tale style, children gathered under a big tree sharing their lunchboxes, "
                        "with sunlight filtering through the leaves."
                    ),
                    "image_path": "/images/story_user002_cut_2.png"
                }
            ]
        },
        "user003": {
            "story_text": """
                어릴 적에는 겨울이 참 추웠어요. 눈이 소복이 쌓인 들판을 지나 학교로 가는 길은 힘들었지만, 
                눈싸움을 하며 웃던 친구들의 모습이 아직도 눈에 선합니다.
            """,
            "cuts": [
                {
                    "description": "눈 덮인 들판을 지나가는 아이들.",
                    "image_prompt": (
                        "Fairy tale style, children walking through a snow-covered field, "
                        "bundled up in warm clothes, with soft snowflakes falling from the sky."
                    ),
                    "image_path": "/images/story_user003_cut_1.png"
                },
                {
                    "description": "친구들과 함께 눈싸움을 하는 모습.",
                    "image_prompt": (
                        "Fairy tale style, children laughing and throwing snowballs in a snowy playground, "
                        "surrounded by white snow and pine trees."
                    ),
                    "image_path": "/images/story_user003_cut_2.png"
                }
            ]
        }
    }

    for user_id, story_data in user_stories.items():
        # 스토리 생성
        story = Story(
            session_id=f"story_{user_id}",
            title=f"{users[int(user_id[-1]) - 1].name}님의 추억 이야기",
            story_text=story_data["story_text"],
            recommendations=0,
            views=0,
            user_id=user_id,
        )
        db.add(story)
        db.commit()

        # 스토리 컷 생성
        cuts = [
            StoryCut(
                story_id=story.session_id,
                description=cut["description"],
                image_prompt=cut["image_prompt"],
                image_path=cut["image_path"],
            )
            for cut in story_data["cuts"]
        ]
        db.add_all(cuts)
        db.commit()

# 실행
create_dummy_data()
print("사용자 별 더미 데이터가 성공적으로 생성되었습니다!")

# 세션 닫기
db.close()