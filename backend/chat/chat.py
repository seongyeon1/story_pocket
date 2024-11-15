from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

from common import *
from .prompts import *

from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

# 프롬프트 정의
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        # 대화기록용 key 인 chat_history 는 가급적 변경 없이 사용하세요!
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "#Sex:\n{sex}\n\n#Message:\n{message}"),  # 사용자 입력을 변수로 사용
    ]
)

# llm 생성
# llm = ChatOpenAI(model_name="gpt-4o-mini")
llm = gpt_4o_mini
# llm = gemini_1_5_flash

# 일반 Chain 생성
chain = prompt | llm | StrOutputParser()

from .tools import *

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