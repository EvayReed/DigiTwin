from translate import Translator
from typing import Union
from app.tool.base import BaseTool

# # 创建翻译器对象
# translator = Translator(from_lang="zh", to_lang="en")
#
# # 翻译文本
# translation = translator.translate("你好，世界")
#
# print(translation)  # 输出翻译结果

class Translatertool(BaseTool):
    name: str = "translater"
    description: str = """Perform text translation between languages using modified rules.
    -target language, 
    -text to be translated，
    as inputs.
    """
    parameters: dict = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "(required) Text content to translate"
            },
            "target_lang": {
                "type": "string",
                "enum": ["zh", "en", "ja", "ko", "fr"],
                "default": "zh",
                "description": "Target language (default: Chinese)"
            }
        },
        "required": ["text"]
    }

    async def execute(self,
                      text: str,
                      target_lang: str = "zh") -> str:

        try:
            # Initialize translator with enhanced configuration
            translator = Translator(
                to_lang=target_lang,
                # from_lang='auto',
                # secret_access_key='your_api_key',  # 实际使用时应从配置读取
                # provider='microsoft',  # 可选提供商：google, mymemory
            )
            translation = translator.translate(text)
            return translation
        except ConnectionError:
            return "翻译错误：无法连接翻译服务，请检查网络连接"
        except ValueError as e:
            return f"翻译参数错误：{str(e)}"
        except Exception as e:
            return f"翻译异常：{str(e)}"




