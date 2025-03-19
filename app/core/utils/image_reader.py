import requests
import json


def ocr_request(encoded_string):
    url = "http://47.115.33.23:1224/api/ocr"
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
        return res_dict  # 返回 OCR 请求的结果
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


# 示例使用
encoded_string = "your_encoded_base64_string_here"
result = ocr_request(encoded_string)
if result:
    print(result)
