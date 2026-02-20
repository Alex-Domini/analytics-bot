from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    BOT_TOKEN: str

    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: Literal["openai", "fake", "local"] = "fake"

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def check_openai_key(cls, v: str, info):
        if v == "your_key_here" or not v.startswith("sk-"):
            raise ValueError(
                "Вы забыли заменить 'your_key_here' на реальный ключ OpenAI в файле .env!"
            )
        return v

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return self.DATABASE_URL.replace("+asyncpg", "")


settings = Settings()  # type: ignore
