import logging

import requests
import json
from langchain_core.prompts import PromptTemplate

from app.core.prompts.system import echarts_render_prompt, orc_prompt
from app.services.llm_service import ai_engine


def ocr_request(encoded_string):
    url = "http://localhost:1224/api/ocr"
    data = {
        "base64": encoded_string,
        "options": {
            "data.format": "text",
        }
    }
    headers = {"Content-Type": "application/json"}
    data_str = json.dumps(data)

    try:
        response = requests.post(url, data=data_str, headers=headers)
        response.raise_for_status()
        res_dict = json.loads(response.text)
        image_info = res_dict.get("data")
        logging.error("=================================================================================================", image_info)
        llm = ai_engine.get_openai_model()
        chart_code = llm.invoke(orc_prompt.format(query=image_info))
        image_content = chart_code.content.strip()
        return image_content, image_info
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}", e)
        print(f"Request failed: {e}")
        return None
