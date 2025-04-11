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


result1 = chart("""
| 1    | 收入     | 2000  | 公司A  | 2025-04-30 10:00   |
| 2    | 支出     | 500   | 餐厅B  | 2025-04-29 15:00   |
| 3    | 收入     | 1500  | 公司C  | 2025-04-28 12:00   |
| 4    | 支出     | 300   | 超市D  | 2025-04-27 09:00   |
| 5    | 支出     | 700   | 餐厅E  | 2025-04-26 18:00   |
""")

print(result1)
