import logging

from langchain.schema import HumanMessage

from app.core.prompts.system import echarts_eligibility_prompt, echarts_render_prompt
from app.services.llm_service import ai_engine


def chart(query: str) -> bool:
    llm = ai_engine.get_openai_model()
    response = llm.invoke(echarts_eligibility_prompt.format(query=query))
    result = response.content.strip()
    is_chart_data_available = result == "1"
    if is_chart_data_available:
        chart_code = llm.invoke(echarts_render_prompt.format(query=query))
        return chart_code.content.strip()
    else:
        return None
