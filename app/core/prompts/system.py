from langchain.prompts import PromptTemplate

HINT = "你觉得我可能还会问你什么问题，请把你猜测的可能的问题用^号分隔开告诉我，除了答案不要有类似‘好的，我会尽量猜测你可能会问的问题。以下是我的猜测：’这样的的字符出现"

echarts_eligibility_prompt = PromptTemplate.from_template("""
根据以下内容分析是否具备绘制 ECharts 图表的条件和数据：{query}；请回答 0（不具备）或 1（具备）；只能回答一个字符。
""")

# echarts_render_prompt = PromptTemplate.from_template("""
# 请根据以下数据渲染一个或多个ECharts图表，你帮我选择柱状图、折线图、饼状图、动态轨迹图、日历图、极坐标图、树图、旭日图、关系图、散点图、面积图、热力图以及玫瑰图的呈现方式；按照纵向排列，并用 HTML 编码。{query}
# 请确保返回的仅是 HTML 代码，不包含其他说明文字或文件格式提示；字符串前后不要有反引号（`）。
# """)

echarts_render_prompt = PromptTemplate.from_template("""
你将根据以下数据生成一个或多个适合的 ECharts 图表，图表类型可从以下列表中智能选择：柱状图、折线图、饼状图、动态轨迹图、日历图、极坐标图、树图、旭日图、关系图、散点图、面积图、热力图、玫瑰图。

请自动选择最合适的图表类型，并以纵向排列的方式用 HTML 编写完整代码。确保输出仅包含 HTML 代码，无任何说明、解释或其他标记字符（如反引号）。

以下是数据或需求描述：
{query}
""")

