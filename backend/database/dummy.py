from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from models import Base, User, Story, StoryCut, engine

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 세션 생성
db = Session(bind=engine)

# 더미 데이터 생성
def create_story_and_cuts():
    # 1. 사용자 생성
    user = User(
        user_id="user_seongwoo",
        name="김성우",
        password="password123",
        phone="01016863569",
        birth_date=date.today() - timedelta(days=60 * 365),  # 60세
        gender="남성",
        join_date=datetime.utcnow()
    )
    db.add(user)
    db.commit()

    # 2. 스토리 생성
    story_text = """
    옛날, 지금 60대가 된 성우 할아버지와 미영 할머니가 아주 젊고 풋풋했던 시절의 이야기야. 성우 할아버지와 미영 할머니는 20대 시절, 서울에 막 올라와서 바쁘게 일하며 꿈을 키우던 청춘들이었어. 그 당시엔 인터넷도, 스마트폰도 없었고, 편지도 직접 써야 했던 시절이었지.

성우 할아버지는 공장에서 일을 했고, 미영 할머니는 작은 상점에서 일했어. 둘은 지하철역에서 우연히 만나 인사를 나누고, 몇 번이고 그곳에서 다시 만나게 되었지. 그 후론 둘이 서로에게 기대며 조금씩 친구가 되었어.

어느 날, 성우 할아버지는 큰 용기를 내서 미영 할머니에게 데이트 신청을 했어. “혹시 이번 주말에 남산에 같이 갈래요?” 미영 할머니는 수줍게 고개를 끄덕였지. 주말이 되자, 둘은 손을 잡고 남산으로 올라갔어. 그때는 지금처럼 케이블카도 흔하지 않아서, 땀을 뻘뻘 흘리며 산길을 따라 걸어 올라가야 했어. 두 사람은 산을 오르며 서로의 이야기를 나누었고, 또 세상을 바라보는 마음도 비슷하다는 걸 느꼈지.

남산 정상에 도착했을 때, 미영 할머니는 서울의 모습을 내려다보며 깊이 숨을 들이쉬었어. 성우 할아버지는 갑자기 주머니에서 작은 봉투를 꺼냈어. “이건, 내가 공장에서 번 돈으로 산 거예요.” 그 안에는 빨간색 손수건이 들어 있었어. 성우 할아버지는 “이거면 다음에 힘들 때 서로 닦아 줄 수 있지 않겠어요?”라고 웃으며 손수건을 건넸지.

그 손수건은 두 사람에게 소중한 보물이 되었어. 성우 할아버지가 힘들 때마다 미영 할머니는 그 손수건을 꺼내서 성우 할아버지의 땀을 닦아주었어. 시간이 흘러 두 사람은 결혼을 하고, 아이들도 생기고, 어려운 일도 많았지만 서로를 지켜주는 든든한 힘이 되었어.

이제 성우 할아버지와 미영 할머니는 손주들이 찾아올 때마다 그 빨간 손수건 이야기를 해 주며 웃곤 한단다. 그 빨간 손수건은 지금도 서랍 속에 조심스럽게 간직되어 있대. 손주들이 “할아버지, 이 손수건이 그렇게 특별해요?”라고 물으면, 할아버지와 할머니는 서로를 보며 눈웃음을 지어. “우리에게는 이 손수건이 가장 소중한 보물이란다. 너희도 꼭 지켜줄 사람이 생기면, 이렇게 작은 보물을 만들렴.” 하고 말해준단다.

지금은 옛날처럼 빨간 손수건을 꼭 챙기지 않아도, 그 손수건은 두 사람의 마음속에서 항상 빛나고 있어.
    """
    story = Story(
        session_id="story_seongwoo",
        title="성우 할아버지와 미영 할머니의 사랑 이야기",
        story_text=story_text.strip(),
        recommendations=0,
        views=0,
        user_id=user.user_id
    )
    db.add(story)
    db.commit()

    # 3. 스토리 컷 생성
    cuts = [
        StoryCut(
            story_id=story.session_id,
            description="성우 할아버지와 미영 할머니의 첫 만남",
            image_prompt=(
                "Fairy tale style, a bustling subway station in 1960s Seoul, filled with people wearing vintage clothing. "
                "Among the crowd, young Seongwoo and Miyoung exchange shy smiles for the first time."
            ),
            image_path="/images/story_seongwoo_cut_1.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="성우 할아버지가 데이트 신청하는 장면",
            image_prompt=(
                "Fairy tale style, Seongwoo in a neatly pressed suit nervously holding a small flower, "
                "standing in front of Miyoung on a busy street in 1960s Seoul."
            ),
            image_path="/images/story_seongwoo_cut_2.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="남산 산길을 함께 걷는 두 사람",
            image_prompt=(
                "Fairy tale style, Seongwoo and Miyoung walking hand-in-hand along a rustic trail on Namsan Mountain, "
                "surrounded by lush greenery and blooming flowers."
            ),
            image_path="/images/story_seongwoo_cut_3.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="남산 정상에서 성우 할아버지가 빨간 손수건을 건네는 장면",
            image_prompt=(
                "Fairy tale style, Seongwoo offering a beautifully folded red handkerchief to Miyoung, "
                "overlooking the stunning skyline of Seoul during sunset."
            ),
            image_path="/images/story_seongwoo_cut_4.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="미영 할머니가 성우 할아버지의 땀을 닦아주는 장면",
            image_prompt=(
                "Fairy tale style, Miyoung gently wiping Seongwoo's forehead with the treasured red handkerchief "
                "in their modest 1960s home."
            ),
            image_path="/images/story_seongwoo_cut_5.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="두 사람이 결혼하고 가족을 이루는 모습",
            image_prompt=(
                "Fairy tale style, a heartfelt wedding ceremony in the 1970s, with Seongwoo and Miyoung surrounded by friends and family."
            ),
            image_path="/images/story_seongwoo_cut_6.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="손주들에게 빨간 손수건 이야기를 들려주는 장면",
            image_prompt=(
                "Fairy tale style, Seongwoo and Miyoung sitting in their cozy living room, surrounded by curious grandchildren, "
                "telling the story of the red handkerchief."
            ),
            image_path="/images/story_seongwoo_cut_7.png"
        ),
        StoryCut(
            story_id=story.session_id,
            description="빨간 손수건이 서랍 속에 소중하게 간직된 장면",
            image_prompt=(
                "Fairy tale style, a well-worn red handkerchief folded carefully in an old wooden drawer, "
                "surrounded by cherished letters and small trinkets."
            ),
            image_path="/images/story_seongwoo_cut_8.png"
        ),
    ]
    db.add_all(cuts)
    db.commit()

# 실행
create_story_and_cuts()
print("성우 할아버지와 미영 할머니의 이야기가 성공적으로 생성되었습니다!")

# 세션 닫기
db.close()