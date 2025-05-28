from pandasai_litellm import LiteLLM

from langchain.chat_models import init_chat_model
from langchain_ollama.chat_models import ChatOllama


def get_llm_pandasai():
    llm = LiteLLM(model="ollama/qwen2.5")
    return llm


def get_llm():
    return init_chat_model("qwen2.5", model_provider="ollama")


def get_llm_bind_support():
    return ChatOllama(model="qwen2.5")
