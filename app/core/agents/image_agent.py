from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import SceneXplainTool

from app.services.llm_service import ai_engine

tool = SceneXplainTool()

memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    [tool], ai_engine.get_openai_model(), memory=memory, agent="conversational-react-description", verbose=True
)
output = agent.run(
    input=(
        "What is in this image https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F0rw369i5h9t%2Foriginal.png. "
        "Is it movie or a game? If it is a movie, what is the name of the movie?"
    )
)