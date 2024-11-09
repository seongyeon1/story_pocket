from .prompts import *
from common import *
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = gemini_pro

story_prompt = PromptTemplate(
    template=story_template,
    input_variables=["story"]
)

story_chain = story_prompt | llm | StrOutputParser()
