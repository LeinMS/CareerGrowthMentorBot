
from ugc.db_func import ProfileInterface, MessageInterface
# from dotenv import load_dotenv
# import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts.prompt import PromptTemplate
from ugc.Templates import default_bot_template_1, default_bot_template_2, default_user_template, bot_history
from langchain.schema import AIMessage, HumanMessage
from langchain.memory import ChatMessageHistory
from django.conf import settings


def load_chat_model():
    openai.api_key = settings.OPENAI_API_KEY
    llm = ChatOpenAI(model_name='gpt-4', temperature=0.9)
    return llm

def init_prompt_template(user_prompt: str = None):
    """Инициализируем шаблон бота с пользовательским шаблоном."""
    if user_prompt != None:
        prompt = PromptTemplate(input_variables=["history", "input"], template=default_bot_template_1 + user_prompt + default_bot_template_2 + bot_history)
        return prompt
    else:
        prompt = PromptTemplate(input_variables=["history", "input"], template=default_bot_template_1 + default_user_template + default_bot_template_2 + bot_history)
        return prompt


def init_conversation_chain(llm, prompt):
    memory = ConversationBufferWindowMemory(k=3, return_messages=True, ai_prefix="SensEI")
    conversation = ConversationChain(prompt=prompt, llm=llm, memory=memory)
    return conversation


def init():
    # Load the OpenAI API key from the environment variable
    # load_dotenv()
    if settings.OPENAI_API_KEY is None or settings.OPENAI_API_KEY == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")


def get_user_template():
    user_template = default_user_template
    return user_template


# Функция get_conversation теперь принимает два аргумента: user_prompt и profile
def get_conversation(user_prompt: str, profile: ProfileInterface):
    try:
        init()
        llm = load_chat_model()

        prompt = init_prompt_template(user_prompt)

        # Загрузка последних записей из базы данных для данного профиля
        last_n_entries = MessageInterface.get_last_n_entries(profile)

        # Преобразование записей из базы данных в формат, который требуется для ConversationBufferWindowMemory
        messages = []
        for entry in last_n_entries:
            # Сначала добавляем сообщение пользователя, затем ответ бота
            messages.append(HumanMessage(content=entry.user_text, additional_kwargs={}, example=False))
            messages.append(AIMessage(content=entry.bot_answer, additional_kwargs={}, example=False))

        # Инициализация буфера памяти с загруженными сообщениями
        memory = ConversationBufferWindowMemory(k=6, return_messages=True, ai_prefix="SensEI", chat_memory=ChatMessageHistory(messages=messages))
        conversation = ConversationChain(prompt=prompt, llm=llm, memory=memory)

        return conversation

    except Exception as e:
        print(f"Error in get_conversation: {e}")
        # Возвращаем None или какое-либо другое значение по умолчанию, чтобы обозначить, что произошла ошибка
        return None
