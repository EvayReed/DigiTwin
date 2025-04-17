import logging

import requests
import json
from langchain_core.prompts import PromptTemplate

from app.services.llm_service import ai_engine


def ocr_request(encoded_string):
    url = "http://127.0.0.1:1224/api/ocr"
    data = {
        "base64": encoded_string,
        # 可选参数示例
        "options": {
            "data.format": "text",
        }
    }
    headers = {"Content-Type": "application/json"}
    data_str = json.dumps(data)

    try:
        response = requests.post(url, data=data_str, headers=headers)
        response.raise_for_status()  # 如果响应返回错误状态码，抛出异常
        res_dict = json.loads(response.text)
        prompt_template = PromptTemplate(
            input_variables=["content"],
            template="以下是图片识别得到的信息。请以key，value的形式把所得信息加工后返回：{content}"
        )
        logging.error("图片信息", res_dict)
        chain = prompt_template | ai_engine.get_openai_model()

        image_content = chain.invoke({"content": res_dict})
        return image_content, res_dict
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
