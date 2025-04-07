from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain.schema import SystemMessage, HumanMessage

from app.services.llm_service import ai_engine


class PromptRouterChain:
    def __init__(self, prompt_dict):
        self.prompts = prompt_dict
        self.model = ai_engine.get_openai_model()
        self.embedding_model = ai_engine.get_embedding_model()
        self.prompt_embeddings = {
            name: self.embedding_model.embed_query(prompt)
            for name, prompt in self.prompts.items()
        }

    def route_prompt(self, user_input):
        user_embedding = self.embedding_model.embed_query(user_input)
        similarities = {
            name: cosine_similarity([user_embedding], [embedding])[0][0]
            for name, embedding in self.prompt_embeddings.items()
        }
        best_prompt_name = max(similarities, key=similarities.get)
        return best_prompt_name, self.prompts[best_prompt_name]

    def run(self, user_input):
        best_prompt_name, selected_prompt = self.route_prompt(user_input)
        messages = [
            SystemMessage(content=selected_prompt),
            HumanMessage(content=user_input)
        ]
        response = self.model(messages)
        return {
            "selected_prompt": best_prompt_name,
            "response": response.content
        }


# 示例 Prompt
prompt_dict = {
    "local_guide": "你是一位当地原居民，根据用户提供的出行地点和想法，提供出行方案。\n[输入] ...",
    "female_guide": "你是一位当资深的女性导游，根据用户提供的出行地点和想法，提供出行方案。\n#思考 ...",
    "doc_check": "###输入\n**证件信息：**\n- 证件名称：{...}",
    "doc_suggestion": "### 输出-已上传\n1. 概述：..."
}

# 示例调用
if __name__ == "__main__":
    router_chain = PromptRouterChain(prompt_dict)
    user_input = "我的身份证什么时候到期？"
    result = router_chain.run(user_input)
    print(f"【匹配到的提示词】：{result['selected_prompt']}")
    print(f"【生成结果】：\n{result['response']}")
