from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage 
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI()

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
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "#Sex:\n{sex}\n\n#Message:\n{message}"),
    ]
)

# LLM 생성
llm = ChatOpenAI(model_name="gpt-4o-mini")


# 일반 Chain 생성
chain = prompt | llm | StrOutputParser()

# 세션 기록을 저장할 딕셔너리
store = {}

# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id):
    if session_id not in store:  # 세션 ID가 store에 없는 경우
        store[session_id] = ChatMessageHistory()  # 새로운 세션 기록 생성
    return store[session_id]  # 세션 기록 반환

# Chain에 세션 기록을 추가한 객체
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="message",
    history_messages_key="chat_history",
)

# FastAPI 요청 모델 정의
class ChatRequest(BaseModel):
    sex: str
    message: str
    session_id: str

# 다중 대화 함수 정의
def multi_turn_chat(sex, message, session_id):
    return chain_with_history.invoke(
        {"sex": sex, "message": message},
        config={"configurable": {"session_id": session_id}},
    )

# 이야기 템플릿
story_template = """
    할아버지의 그 때 그 시절의 일을 이야기로 다시 만들어줘
    공감이 잘 되도록 현장감있게 사건을 묘사해줘
    아이의 말은 없애고 할아버지가 혼자 나레이션처럼 말하는 형식으로 수정해줘
    -----
    이야기 : {story}
"""
story_prompt = PromptTemplate(
    template=story_template,
    input_variables=["story"]
)

story_chain = story_prompt | llm | StrOutputParser()

# API 엔드포인트 정의 (대화 생성)
@app.post("/chat/")
async def chat(request: ChatRequest):
    response = multi_turn_chat(request.sex, request.message, request.session_id)
    return {"response": response}

# 전체 대화 기록을 조회하는 API 엔드포인트 정의
@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    # 해당 session_id가 존재하지 않으면 에러 반환
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    # 비동기적으로 대화 히스토리 가져오기
    chat_history = await store[session_id].aget_messages()
    
    # 메시지의 종류에 따라 역할(role)을 지정해 대화 기록 반환
    history = [
        {
            "role": "user" if isinstance(msg, HumanMessage) else "ai",
            "content": msg.content
        }
        for msg in chat_history
    ]
    
    return {"session_id": session_id, "history": history}


# 전체 대화 기록을 조회하고 이야기로 변환하는 API 엔드포인트 정의
@app.get("/story/{session_id}")
async def get_story(session_id: str):
    # 해당 session_id가 존재하지 않으면 에러 반환
    if session_id not in store:
        raise HTTPException(status_code=404, detail="Session ID not found")
    
    # 비동기적으로 대화 히스토리 가져오기
    chat_history = await store[session_id].aget_messages()
    
    # 대화 내용을 story 형식으로 변환
    story = "\n".join([msg.content for msg in chat_history if isinstance(msg, (HumanMessage, AIMessage))])
    
    # story를 템플릿을 이용해 할아버지의 이야기 형식으로 변환
    final_story = story_chain.invoke({"story": story})
    
    return {"session_id": session_id, "story": final_story}