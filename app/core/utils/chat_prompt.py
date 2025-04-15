from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime

from app.services.llm_service import ai_engine

main_prompt = """
你是一个智能助手，帮助用户提供个性化的旅行建议。你的任务是根据用户的需求、位置、兴趣等信息来推荐最合适的旅行计划。
当前的日期和时间是：{current_time}
"""


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


prompt_template = PromptTemplate(
    input_variables=["current_time", "question"],
    template=main_prompt + "\n\n用户的问题是：{question}\n\n请生成一个回复。"
)

llm = ai_engine.get_openai_model()

llm_chain = LLMChain(prompt=prompt_template, llm=llm)

# User query
user_question = "我想去巴黎旅行，推荐一些活动。"
current_time = get_current_time()  # Get the current time

# Generate an answer
answer = llm_chain.invoke({"current_time": current_time, "question": user_question})
print(answer)
