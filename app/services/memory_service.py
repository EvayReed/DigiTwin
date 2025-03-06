import uuid
from langchain.llms import OpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.language_models.llms import BaseLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage


class RunnableHistoryMemory:
    def __init__(self, model: BaseLLM, prompt: ChatPromptTemplate = None,session:str = None):
        """
        Initializes the encapsulation class
        :param history_function: The function used to retrieve history records
        :param model: The language model to be used (e.g., text-davinci-003)
        :param prompt: The chat prompt template
        """
        try:
            # Create chat prompt template
            if prompt is None:
                self.prompt = self.get_prompt()
            else:
                self.prompt = prompt
            # Create runnable
            self.runnable = self.prompt | model
            # Create session
            if session is None:
                self.session = self.generate_random_session()
            else:
                self.session = session
            # Encapsulate into RunnableWithMessageHistory with history
            self.runnable_with_history = RunnableWithMessageHistory(
                self.runnable,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="history",
            )

        except TypeError as e:
            # Handle type errors (e.g., incorrect input types for prompt, model, or history_function)
            print(
                f"TypeError: {str(e)} - Please ensure all parameters are of the correct type (e.g., prompt, model, history_function)")
        except AttributeError as e:
            # Handle attribute errors (e.g., missing required attributes or methods)
            print(
                f"AttributeError: {str(e)} - Ensure all required attributes or methods exist and are initialized properly")
        except Exception as e:
            # Handle other unknown errors
            print(
                f"Unknown error: {str(e)} - There was an issue with the initialization, please check input parameters and configurations.")

    def generate_random_session(self):
        """
        Generates a random session ID
        :return: A randomly generated session ID (UUID)
        """
        try:
            # Generate a random session ID using UUID
            session_id = str(uuid.uuid4())
            return session_id

        except Exception as e:
            # Handle any potential errors in session ID generation
            print(f"Error generating session ID: {str(e)} - Please check the UUID generation process.")
            return None

    def process_input(self, input_text: str, language: str = "english"):
        """
        Processes the input text and returns a response
        :param input_text: The text input from the user
        :param session_id: The session ID used for retrieving historical records
        :param language: The language type, default is English
        :return: The generated response
        """
        try:
            # Pass input and history to runnable
            response = self.runnable_with_history.invoke(
          {"language": language, "input": input_text},
                config={"configurable": {"session_id": self.session}})

            # Return the generated response
            return response

        except AttributeError as e:
            # Handle attribute errors (e.g., incorrect initialization of runnable_with_history)
            return {
                "error": f"AttributeError: {str(e)} - Please check if runnable_with_history is correctly initialized"}
        except TypeError as e:
            # Handle type errors (e.g., incorrect input type)
            return {"error": f"TypeError: {str(e)} - The input type might not be correct"}
        except Exception as e:
            # Handle other unknown errors
            return {"error": f"Unknown error: {str(e)} - Please check the input and system configuration"}

    def get_prompt(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You're an assistant who speaks in {language}. Respond in 20 words or fewer",
                ),
                MessagesPlaceholder(variable_name="history",n_messages=5),
                ("human", "{input}"),
            ]
        )
        return prompt

# 定义一个函数，用于获取会话历史
    def get_session_history(self,session_id):
        # 返回一个SQLChatMessageHistory对象，参数为会话ID和数据库路径
        return SQLChatMessageHistory(session_id, "sqlite:///memory.db")


