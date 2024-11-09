from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


# 환경 변수 로드
load_dotenv()

# GPT-4o-mini 모델 설정
gpt_4o_mini = ChatOpenAI(
    temperature=0, 
    model_name="gpt-4o-mini",
    # streaming=True,              
    # callbacks=[StreamingStdOutCallbackHandler()]
)

# gemini-1.5-flash 모델 설정
gemini_1_5_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)
gemini_pro = ChatGoogleGenerativeAI(model="gemini-pro")
# gemini_1_5_flash = GoogleGenerativeAI(model="gemini-1.5-flash")  # 메타클래스 오류 발생 시 주석 처리