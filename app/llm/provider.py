# import os
from app.llm.fake_client import FakeLLMService

# from app.llm.openai_client import OpenAILLMService
# from app.llm.local_client import LocalLLMService


def get_llm_service():
    # provider = os.getenv("LLM_PROVIDER", "fake")

    # # if provider == "openai":
    # #     return OpenAILLMService
    # if provider == "local":
    #     return LocalLLMService

    return FakeLLMService()
