from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

max_iterations = 3
recursion_limit = 2 * max_iterations + 1
agent = create_react_agent(
    model="anthropic:claude-3-5-haiku-latest",
    tools=[get_weather]
)

try:
    response = agent.invoke(
        {"messages": "what's the weather in sf"},
        {"recursion_limit": recursion_limit},
    )
except GraphRecursionError:
    print("Agent stopped due to max iterations.")