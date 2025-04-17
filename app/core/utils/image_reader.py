import logging

import requests
import json
from langchain_core.prompts import PromptTemplate

from app.services.llm_service import ai_engine


def ocr_request(encoded_string):
    url = "http://127.0.0.1:1224/api/ocr"
    data = {
        # "base64": encoded_string,
        "base64": "iVBORw0KGgoAAAANSUhEUgAAAC4AAAAXCAIAAAD7ruoFAAAACXBIWXMAABnWAAAZ1gEY0crtAAAAEXRFWHRTb2Z0d2FyZQBTbmlwYXN0ZV0Xzt0AAAHjSURBVEiJ7ZYrcsMwEEBXnR7FLuj0BPIJHJOi0DAZ2qSsMCxEgjYrDQqJdALrBJ2ASndRgeNI8ledutOCLrLl1e7T/mRkjIG/IXe/DWBldRTNEoQSpgNURe5puiiaJehrMuJSXSTgbaby0A1WzLrCCQCmyn0FwoN0V06QONWAt1nUxfnjHYA8p65GjhDKxcjedVH6JOejBPwYh21eE0Wzfe0tqIsEkGXcVcpoMH4CRZ+P0lsQp/pWJ4ripf1XFDFe8GHSHlYcSo9Es31t60RdFlN1RUmrma5oTzTVB8ZUaeeYEC9GmL6kNkDw9BANAQYo3xTNdqUkvHq+rYhDKW0Bj3RSEIpmyWyBaZaMTCrCK+tJ5Jsa07fs3E7esE66HzralRLgJKp0/BD6fJRSxvmDsb6joqkcFXGqMVVFFEHDL2gTxwCAaTabnkFUWhDCHTd9iYrGcAL1ZnqIp5Vpiqh7bCfua7FA4qN0INMcN1+cgCzj+UFxtbmvwdZvGIrI41JiqhZBWhhF8WxorkYPpQwJiWYJeA3rXE4hzcwJ+B96F9zCFHC0FcVegghvFul7oeEE8PvHeJqC0w0AUbbFIT8JnEwGbPKcS2OxU3HMTqD0r4wgEIuiKJ7i4MS16+og8/+bPZRPLa+6Ld2DSzcAAAAASUVORK5CYII=",
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
        logging.error("这里是图片信息", res_dict)
        chain = prompt_template | ai_engine.get_openai_model()

        image_content = chain.invoke({"content": res_dict})
        return image_content, res_dict
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
