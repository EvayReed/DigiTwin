import asyncio
import json
from typing import Generic, Optional, TypeVar

from browser_use import Browser as BrowserUseBrowser
from browser_use import BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use.dom.service import DomService
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from app.config import config
from app.llm import LLM
from app.tool.base import BaseTool, ToolResult
from app.tool.web_search import WebSearch

import plotly.express as px
import pandas as pd


class PlotlyUseTool(BaseTool):
    name: str = "plotlyuse"
    description: str = """Generate interactive Plotly visualizations based on data and chart type.
    - generate raw_data in JSON format {x:[],y:[]} for the chart based on the content provided by the user, and generate data according to different types of charts.
    "JSON containing columns matching chart type requirements. Example formats:\n"
                               "- Scatter/Bar/Line: {x: [...], y: [...]}\n"
                               "- Pie: {names: [...], values: [...]}\n"
                               "- Polar: {r: [...], theta: [...]}",
                               
    - Automatically selects appropriate visualization parameters
    - Returns both raw data and generated figure object"""
    
    parameters: dict = {
        "type": "object",
        "properties": {
            "plotlytype": {
                "type": "string",
                "enum": [
                    "scatter",  # 散点图 (需x,y)
                    "bar",      # 柱状图 (需x,y)
                    "line",     # 折线图 (需x,y) 
                    "area",     # 面积图 (需x,y)
                    "pie",      # 饼图 (需names,values)
                    "line_polar",   # 雷达图 (需r,theta)
                    "scatter_polar",# 极坐标散点图 (需r,theta)
                ],
                "description": "Plotly chart type with required data columns in parentheses",
            },
            "raw_data": {
                "type": "object",
                "description": "DataFrame containing columns matching chart type requirements. Example formats:\n"
                               "- Scatter/Bar/Line: {x: [...], y: [...]}\n"
                               "- Pie: {names: [...], values: [...]}\n"
                               "- Polar: {r: [...], theta: [...]}",
            },
            "title": {
                "type": "string",
                "description": "(optional) Chart title text"
            }
        },
        "required": ["plotlytype", "raw_data"]
    }

    async def execute(self, plotlytype: str, raw_data: dict, title: str = None) -> dict:
        """
        Generate Plotly visualization with type validation and auto-layout
        
        Args:
            plotlytype: Predefined chart type identifier
            data: Input data with required columns
            title: Optional display title

        Returns:
            dict: {
                "data": original_data,
                "figure": plotly_graph_object,
                "chart_type": plotlytype,
                "status": "success/error"
            }
        """
        try:
            # 新增数据转换层
            data = pd.DataFrame(raw_data)
            # 数据完整性验证
            required_columns = {
                "scatter": ["x", "y"],
                "bar": ["x", "y"],
                "line": ["x", "y"],
                "area": ["x", "y"],
                "pie": ["names", "values"],
                "line_polar": ["r", "theta"],
                "scatter_polar": ["r", "theta"]
            }.get(plotlytype, [])

            # 动态选择图表类型
            fig = None
            if plotlytype == "scatter":
                fig = px.scatter(data, x='x', y='y')
            elif plotlytype == "bar":
                fig = px.bar(data, x='x', y='y')
            elif plotlytype == "line":
                fig = px.line(data, x='x', y='y')
            elif plotlytype == "area":
                fig = px.area(data, x='x', y='y')
            elif plotlytype == "pie":
                fig = px.pie(data, names='names', values='values')
            elif plotlytype == "line_polar":
                fig = px.line_polar(data, r='r', theta='theta')
            elif plotlytype == "scatter_polar":
                fig = px.scatter_polar(data, r='r', theta='theta')
            else:
                return {
                    "status": f"Error: Unsupported chart type {plotlytype}",
                    "data": data.to_dict(),
                    "chart_type": plotlytype
                }

            # 添加标题
            if title:
                fig.update_layout(title_text=title)
            # 显示图表
            fig.show()
            name = title+".png"
            fig.write_image("./"+name)

            return {
                "status": "success",
                "data": data.to_dict(),
                "figure": fig.to_dict(),  # 转换为可序列化字典
                "chart_type": plotlytype
            }

        except Exception as e:
            return {
                "status": f"Error: {str(e)}",
                "data": data.to_dict() if not data else {},
                "chart_type": plotlytype
            }
