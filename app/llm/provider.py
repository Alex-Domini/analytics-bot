from app.core.config import settings
from app.llm.fake_client import FakeLLMService
from app.llm.openai_client import OpenAILLMService
# from app.llm.local_client import LocalLLMService


def get_llm_service():
    provider = settings.LLM_PROVIDER
    if provider == "openai":
        return OpenAILLMService()
    # if provider == "local":
    #     return LocalLLMService()

    return FakeLLMService()
