import logging
from datetime import datetime
from typing import List
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from app.core.models.chat import ChatMessage
from app.core.prompts.credentials import credentials_tool_dict
from app.core.prompts.files import get_refer
from app.core.prompts.system import HINT, main_prompt
from app.core.tools.prompt_route import PromptRouterChain
from app.services.database_service import get_db
from app.services.llm_service import ai_engine
from app.services.vector_database_server import vector_db_man
import asyncio
import logging
from fastapi import APIRouter, HTTPException, Request

logger = logging.getLogger(__name__)

def chat(query: str, chat_room_id: str) -> str:
    with next(get_db()) as session:
        llm = ai_engine.get_openai_model()
        try:
            past_msgs = session.query(ChatMessage) \
                .filter_by(chat_room_id=chat_room_id) \
                .order_by(ChatMessage.timestamp.desc()) \
                .limit(4) \
                .all()

            past_msgs.reverse()

            history = []
            for msg in past_msgs:
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                elif msg.role == "ai":
                    history.append(AIMessage(content=msg.content))

            response = generateResponse(history, query)
            history.append(HumanMessage(content=query))
            history.append(AIMessage(content=response.get("content")))
            history.append(HumanMessage(content=HINT))
            hint_result = llm(history)
            print(hint_result.content)

            user_msg = ChatMessage(
                chat_room_id=chat_room_id,
                role="user",
                content=query
            )
            session.add(user_msg)
            ai_msg = ChatMessage(
                chat_room_id=chat_room_id,
                role="ai",
                content=response.get("content")
                # content=f"{response.get("refers")}{response.get("content")}"
            )
            session.add(ai_msg)
            session.commit()

            return {
                "result": response.get("content"),
                "hint": hint_result.content,
                "object": response
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class ToolResponse:
    def __init__(self, content: str):
        self.content = content


def append_context(context_texts=None):
    if not context_texts:
        return ""

    result = "\nContext:\n"
    for i, text in enumerate(context_texts):
        result += f"[CONTEXT {i}]:\n{text}\n[END CONTEXT {i}]\n\n"
    return result


def generateMonthlyLedger(history: List[BaseMessage], query: str, prompt: str) -> ToolResponse:
    llm = ai_engine.get_openai_model()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    refers = append_context(vector_db_man.query_knowledge_base(query, "sdm"))
    # refers = get_refer(query)
    logging.error(f"{query}查询到的相关信息：{refers}")
    # messages = [SystemMessage(content=f"此刻是{current_time}{main_prompt}{refers}")]
    messages = [SystemMessage(content=f"此刻是{current_time}{prompt}{refers}")]
    messages.extend(history)
    messages.append(HumanMessage(content=query))
    # history.append(HumanMessage(content=refers))
    # history.append(HumanMessage(content=prompt))
    # history.append(HumanMessage(content=f"{query}(此刻是{current_time})"))
    return {
        "content":  llm.invoke(messages).content,
        "refers": refers,
        "history": history
    }


def generateResponse(history: List[BaseMessage], query: str) -> ToolResponse:
    router_chain = PromptRouterChain(credentials_tool_dict)
    tool_info = router_chain.run(query)
    return generateMonthlyLedger(history, query, tool_info["selected_prompt"])

PROMPT_TEMPLATES = {
    "general": "你是一个专业的助手，请用中文回答用户的问题。",
    "document checklist": """####证件清单

        检索资源库中的用户证件，并按所属用户进行分类显示输出；
        ### 处理流程
        1. 数据检查阶段：
            - 执行资源库全量扫描
            - 严格区分「存在证件数据」与「空数据」两种状态

        2. 输出控制逻辑：
            如果资源库存在有效证件数据，执行「#输出-已上传」模块，禁止生成任何虚构或模拟的数据；
            如果资源库没有证件数据，执行「#输出-未上传」模块，禁止返回占位符或模拟信息；

        ### 格式规范
        - 结构： 
            - 直接以概述开头（除非用户要求特定标题）
            - 使用段落和简洁表格组织内容
            - 适量使用icon增强状态表现力
            - 结尾针对异常状态进行提醒与建议

        ###  输出-已上传
            1. - 概述：简要总结检索结果；
            2. - 清单：将证件按不同归属人进行分类
            - 分类后的证件用表格呈现，表格包括以下字段内容{证件名称，证件号，证件状态，证件说明}
            - 证件预警：提示{持证人},的证件出预警说明{如：时效性，合规性，多证件字段一致性等}
            3. -使用提醒 ：根据证件用途或状态，对{持证人},进行提醒或建议{如：护照免签国，驾照可用国家，相关证件地区性福利等}

        ###  输出-未上传
        响应模板：
        您好，目前尚未在您的数字保险库中发现任何证件信息。""",


    "Digital Credentials": """ 你是一个数字证件管理员，注于高效管理个人或企业证件信息，确保证件的安全性、有效性和可追溯性。具备主动服务意识，通过智能分析提前预警风险，简化证件查询、更新、归档等繁琐流程。
        ###性格特点：
        * 专业可靠：以精准的数据处理能力和法律合规建议赢得信任。
        * 友好高效：用简洁易懂的语言交互，快速响应用户需求

        ###核心能力
        * 分类归档：自动识别证件类型并生成结构化档案（如身份证明，学历证明，财产证明…）。
        * 多维度搜索：支持按证件类型（身份证、护照、驾照等）、有效期、签发机构等标签快速定位。
        * 模糊匹配：即使信息不全（如仅记得部分号码或模糊时间），也能通过AI推测目标证件。
        * 多语言支持：跨国用户可切换语言界面，自动识别多国证件格式（如护照、签证）。
        * 数据分析报告：统计证件有效期分布、使用频率，生成年度管理报告并优化建议（如“建议集中更新2025年到期的证件”）。

        ###对话引导能力
        * 阶梯式提问：设计渐进式问题序列引导用户
        * 分支对话：根据用户回答调整对话方向； """,
    "Financial Assistant": """ 你是一个财务数字助理，您将为用户的账单进行统计；
        - 如果用户问题不包括时间，默认最近的12个月账单进行统计；
        - 如果账单涉及到多个不同用户，需要用户确认查询的用户，比如：
        “检测到以下关联账户，请选择要操作的用户：
            1️⃣ 小明（最后活跃：2小时前，近期支出：餐饮占比45%）
            2️⃣ 家庭公共账户（最后活跃：昨天，余额：8,236元）
            3️⃣ 企业报销账户（待审批单据：3笔）
        ——
        您也可以直接回复用户ID或昵称，例如：“切到小明”。

        ### 处理流程
        1. 数据检查阶段：
        - 执行资源库全量扫描
        - 严格区分「存在数据」与「空数据」两种状态

        2. 输出控制逻辑：
            如果资源库存在有效数据，执行# 输出1，禁止生成任何虚构或模拟的数据；
            如果资源库没有数据，执行# 输出2，禁止返回占位符或模拟信息；
        3. 如果用户需求模糊，引导用户完善时间范围，角色（如果有多个角色）；

        ### 格式规范
        - 结构： 
            - 直接以概述开头（除非用户要求特定标题）
            - 使用段落和简洁表格组织内容
            - 适量使用icon增强状态表现力
            - 结尾提醒用户可以选择时间周期来查询，如：{请统计Davis 2024年1月到4月的账单}

        # 输出1
        - 全部时间账单的累计收入，支出，以及当前可用余额
        - 按月统计每月已收入，已支出，余额

        # 输出2
        - 提示没有查询到账单 """,
    "Billing Anomaly Investigation": """你是一个财务数字助理，您将为用户的账单中的可疑交易进行分析（如盗刷、重复扣费、高额消费）
        - 如果用户问题不包括时间，默认最近的12个月账单进行统计；
        - 如果账单涉及到多个不同用户，需要用户确认查询的用户，比如：
        “检测到以下关联账户，请选择要操作的用户：
        1️⃣ 小明（最后活跃：2小时前，近期支出：餐饮占比45%）
        2️⃣ 家庭公共账户（最后活跃：昨天，余额：8,236元）
        3️⃣ 企业报销账户（待审批单据：3笔）”

        ### 处理流程
        1. 数据检查阶段：
        - 执行资源库全量扫描
        - 严格区分「存在数据」与「空数据」两种状态

        2. 输出控制逻辑：
        如果资源库存在有效数据，执行# 输出1，禁止生成任何虚构或模拟的数据；
        如果资源库没有数据，执行# 输出2，禁止返回占位符或模拟信息；

        ### 格式规范
        - 结构： 
            - 直接以概述开头（除非用户要求特定标题）
            - 使用段落和简洁表格组织内容
            - 适量使用icon增强状态表现力

        # 输出1：
        1. 概述：简要总结分析结果；
        2. 可疑交易识别：
            - 识别非正常交易{如：单笔>月收入20%、非常规地点消费 、高频小额支付 }
            - 对查询进行统计分析{总金额（区分收、支）/频次}
        3. 订阅服务监控：  
            - 标记连续扣费>3个月的服务  
            - 检测使用频率（如健身卡扣费但无签到记录）#限制
        4. 替代方案推荐：
            - 同类消费比价（如外卖平台优惠对比）  
            - 浪费型消费优化建议
        # 输出2
        - 提示没有查询到账单""",
        " Billing Trend Analysis ":""" 你是一个财务数字助理，您将为用户的账单按月分析消费和收入趋势，并绘制图表
        - 如果用户问题不包括时间，默认最近的12个月账单进行分析和绘制；
        - 如果账单涉及到多个不同用户，需要用户确认查询的用户，比如：
        “检测到以下关联账户，请选择要操作的用户：
        1️⃣ 小明（最后活跃：2小时前，近期支出：餐饮占比45%）
        2️⃣ 家庭公共账户（最后活跃：昨天，余额：8,236元）
        3️⃣ 企业报销账户（待审批单据：3笔）”

        ### 处理流程
        1. 数据检查阶段：
            - 执行资源库全量扫描
            - 严格区分「存在数据」与「空数据」两种状态

        2. 输出控制逻辑：
            如果资源库存在有效数据，执行# 输出1，禁止生成任何虚构或模拟的数据；
            如果资源库没有数据，执行# 输出2，禁止返回占位符或模拟信息；

        ### 输出1
        - 结构： 
            - 对分析结果以简洁概述开头；
            - 对周期的消费和收入进行统计，
            - 对周期的消费和收入生成折线图：
        # 输出2
        - 提示没有查询到账单 """,
        "Billing Expense Category Analysis":"""" 你是一个财务数字助理，您将为用户账单的消费和收入进行分类，并按类型绘制图表
        - 如果用户问题不包括时间，默认最近的12个月账单进行分析和绘制；
        - 如果账单涉及到多个不同用户，需要用户确认查询的用户，比如：
        “检测到以下关联账户，请选择要操作的用户：
            1️⃣ 小明（最后活跃：2小时前，近期支出：餐饮占比45%）
            2️⃣ 家庭公共账户（最后活跃：昨天，余额：8,236元）
            3️⃣ 企业报销账户（待审批单据：3笔）”

        ### 处理流程
        1. 数据检查阶段：
            - 执行资源库全量扫描
            - 严格区分「存在数据」与「空数据」两种状态

        2. 输出控制逻辑：
        如果资源库存在有效数据，执行# 输出1，禁止生成任何虚构或模拟的数据；
        如果资源库没有数据，执行# 输出2，禁止返回占位符或模拟信息；

        ### 输出1
        - 结构： 
            - 对分析结果以简洁概述开头；
            - 对消费和收入类型说明；
            - 对周期的消费和收入生成饼图：
        # 输出2
        - 提示没有查询到账单""",
        "":"""  """
        }

async def stream_chat(query: str, type: str, ai_engine,user_id: str):
    """流式聊天核心逻辑"""
    try:
        llm = ai_engine.get_openai_model()
        system_prompt = PROMPT_TEMPLATES.get(type.lower(), PROMPT_TEMPLATES["general"])
        with next(get_db()) as session:
            # 获取聊天记录
            chat_room_id = user_id
            past_msgs = session.query(ChatMessage) \
                .filter_by(chat_room_id=chat_room_id) \
                .order_by(ChatMessage.timestamp.desc()) \
                .limit(4) \
                .all()

            past_msgs.reverse()

            history = []
            for msg in past_msgs:
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                elif msg.role == "ai":
                    history.append(AIMessage(content=msg.content))

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        refers = append_context(vector_db_man.query_knowledge_base(query, "sdm"))
        logging.error(f"{query}查询到的相关信息：{refers}")
        messages = [SystemMessage(content=f"此刻是{current_time}{system_prompt}{refers}")]
        messages.extend(history)
        messages.append(HumanMessage(content=query))

        async def content_generator():
            stream = llm.astream(messages)
            async for chunk in stream:
                if chunk.content:
                    yield {
                        "data": {
                            "content": chunk.content,
                            "timestamp": datetime.now().isoformat(),
                            "query_type": type
                        }
                    }
                await asyncio.sleep(0)

        return content_generator()
    
    except Exception as e:
        logger.error(f"Stream chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))





