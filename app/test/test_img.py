import base64
import os
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
from app.services.llm_service import ai_engine

# load_dotenv()

def analyze_image(image_path: str, max_tokens: int = 1000) -> Optional[str]:
    """
    使用OpenAI视觉API识别图片内容和文字（2025年新版）

    参数:
        image_path: 图片文件路径
        max_tokens: 最大返回token数（建议2000-4000）

    返回:
        str: 图片描述和文字内容
    """
    try:
        # 编码图片为base64（增加MIME类型校验）
        def encode_image(image_path: str) -> str:
            _, ext = os.path.splitext(image_path)
            mime_type = "image/png" if ext.lower() == ".png" else "image/jpeg"
            with open(image_path, "rb") as image_file:
                return f"data:{mime_type};base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

        base64_image = encode_image(image_path)

        llm = ai_engine.get_img_model()
        # 初始化客户端（推荐使用v3.0+ SDK）
        # client = OpenAI(        # # 调用视觉API（使用最新模型）
        #         # response = client.chat.completions.create(
        #         #     model="gpt-4o",  # 或使用"gpt-4o"
        #         #     messages=[
        #         #         system_prompt,
        #         #         {
        #         #             "role": "user",
        #         #             "content": [
        #         #                 {
        #         #                     "type": "image_url",
        #         #                     "image_url": {
        #         #                         "url": base64_image,
        #         #                         "detail": "high"  # 新增参数
        #         #                     }
        #         #                 }
        #         #             ]
        #         #         }
        #         #     ],
        #         #     max_tokens=max_tokens,
        #         #     temperature=0.2  # 建议添加参数控制输出稳定性
        #         # )
        #     api_key=os.getenv('OPENAI_API_KEY'),
        #     base_url="https://api.openai.com/v1/"  # 新版端点
        # )

        # 构建提示词（符合新版API格式）
#         system_prompt = {
#             "role": "system",
#             "content": """你是一个专业的图像分析助手，请完成以下任务：
# 1. 详细描述图片中的场景、人物、物体及其相互关系
# 2. 识别图片中的所有文字内容（包括招牌、标签、文本等）
# 3. 分析文字与图像的关联性
# 4. 用中文输出结果，保持专业且易于理解的表述"""
#         }
        system_prompt = {
            "role": "system",
            "content": """你是一个专业的图像文字识别助手，请完成以下任务：
        1. 识别图片中的所有文字内容（包括招牌、标签、文本等）
        2. 将文字显示出来并且不包含其他内容"""
        }

        # 调用视觉API（使用最新模型）
        response = llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                system_prompt,
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image,
                                "detail": "high"  # 新增参数
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens,
            temperature=0.2  # 建议添加参数控制输出稳定性
        )

        # # 调用视觉API（使用最新模型）
        # response = client.chat.completions.create(
        #     model="gpt-4o",  # 或使用"gpt-4o"
        #     messages=[
        #         system_prompt,
        #         {
        #             "role": "user",
        #             "content": [
        #                 {
        #                     "type": "image_url",
        #                     "image_url": {
        #                         "url": base64_image,
        #                         "detail": "high"  # 新增参数
        #                     }
        #                 }
        #             ]
        #         }
        #     ],
        #     max_tokens=max_tokens,
        #     temperature=0.2  # 建议添加参数控制输出稳定性
        # )

        return response.choices[0].message.content

    except Exception as e:
        print(f"错误: {str(e)}")
        return None


if __name__ == "__main__":
    # 示例使用
    image_path = "img_1.png"
    result = analyze_image(
        image_path=image_path,
        max_tokens=2000
    )

    if result:
        print("=== 图片分析结果 ===")
        print(result)
    else:
        print("分析失败")

