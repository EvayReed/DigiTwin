import logging

import requests
import json
from langchain_core.prompts import PromptTemplate

from app.services.llm_service import ai_engine


def ocr_request(encoded_string):
    url = "http://localhost:1224/api/ocr"
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
        # response2 = requests.post("http://localhost:1224/api/ocr", data=data_str, headers=headers)
        # if response2.status_code == 200:
        #     logging.error("请求成功")
        #     # 如果返回的是 JSON 数据，可以解析一下：
        #     try:
        #         logging.error(f"status_code状态码：{response2.status_code}")
        #         res_dict = json.loads(response2.text)
        #         logging.error(f"这个出来就对了：{res_dict.get("data")}")
        #         data = response2.json()
        #         logging.error("返回数据：", data)
        #     except ValueError:
        #         logging.error("返回的不是有效的 JSON")
        # else:
        #     logging.error(f"请求失败，状态码：{response2.status_code}")
        #     logging.error("响应内容：", response2.text)

        response.raise_for_status()
        data = response.json()
        logging.error(f"status_code状态码：{response.status_code}")
        res_dict = json.loads(response.text)
        logging.error(f"这个出来就对了：{res_dict.get("data")}")
        prompt_template = PromptTemplate(
            input_variables=["content"],
            template="以下是图片识别得到的信息。请以key，value的形式把所得信息加工后返回：{content}"
        )
        logging.error("这里是图片信息", res_dict.get("data"))
        chain = prompt_template | ai_engine.get_openai_model()

        image_content = chain.invoke({"content": res_dict.get("data")})
        return image_content, res_dict.get("data")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}", e)
        print(f"Request failed: {e}")
        return None
