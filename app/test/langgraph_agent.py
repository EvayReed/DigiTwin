from typing import Annotated, Sequence, TypedDict, List
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从环境变量获取 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")

# 定义状态类型
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "对话历史"]
    next: Annotated[str, "下一步要执行的动作"]

# 定义工具
@tool
def search_tool(query: str) -> str:
    """搜索工具"""
    return f"搜索结果: {query}"

# 创建 LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=OPENAI_API_KEY
)

# 定义节点函数
def agent_node(state: AgentState) -> AgentState:
    """Agent 节点"""
    messages = state["messages"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个发邮件的助手。"),
        ("human", "{input}")
    ])
    response = llm.invoke(prompt.format_messages(input=messages[-1].content))
    return {"messages": [*messages, response]}

def tool_node(state: AgentState) -> AgentState:
    """工具节点"""
    return {"next": "end"}

def end_node(state: AgentState) -> AgentState:
    """结束节点"""
    return state

# 创建工作流
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("agent", agent_node)
workflow.add_node("tool", tool_node)
workflow.add_node("end", end_node)

# 添加边
workflow.add_edge("agent", "tool")
workflow.add_edge("tool", "end")

# 设置入口点
workflow.set_entry_point("agent")

# 设置结束条件
workflow.set_finish_point("end")

# 编译工作流
app = workflow.compile()

# 使用示例
def run_agent(input_text: str):
    """运行 Agent"""
    result = app.invoke({
        "messages": [HumanMessage(content=input_text)],
        "next": "agent"
    })
    return result["messages"][-1].content

if __name__ == "__main__":
    response = run_agent("你好，请帮我搜索一些关于python的信息")
    print(response) 