from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

# 프롬프트 정의
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            당신은 할머니 혹은 할아버지의 이야기를 들어주는 손자입니다.
            아이의 말투로 공감하며 이야기를 들어주세요.
            할머니 혹은 할아버지의 대화를 통해 동화를 만들 예정입니다.
            동화를 만들기 위해 필요한 정보들을 많이 물어봐주세요.
            충분한 정보가 모였다면 자연스럽게 대화를 마무리 할 수 있게 대화합니다.
            성별에 따라 호칭을 맞춰서 불러주세요.
            """,
        ),
        # 대화기록용 key 인 chat_history 는 가급적 변경 없이 사용하세요!
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "#Sex:\n{sex}\n\n#Message:\n{message}"),  # 사용자 입력을 변수로 사용
    ]
)

# llm 생성
llm = ChatOpenAI(model_name="gpt-4o-mini")

# 일반 Chain 생성
chain = prompt | llm | StrOutputParser()

# 세션 기록을 저장할 딕셔너리
store = {}


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    print(f"[대화 세션ID]: {session_ids}")
    if session_ids not in store:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_ids] = ChatMessageHistory()
    return store[session_ids]  # 해당 세션 ID에 대한 세션 기록 반환

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,  # 세션 기록을 가져오는 함수
    input_messages_key="message",  # 사용자의 질문이 템플릿 변수에 들어갈 key
 
    history_messages_key="chat_history",  # 기록 메시지의 키
)

def multi_turn_chat(sex, message, session_id):
    return chain_with_history.invoke(
        # 질문 입력
        {"sex": sex, "message": message},
        # 세션 ID 기준으로 대화를 기록합니다.
        config={"configurable": {"session_id": session_id}},
    )