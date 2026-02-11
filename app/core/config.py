import os


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/analytics",
    )

    @property
    def DATABASE_URL_SYNC(self):
        return self.DATABASE_URL.replace("+asyncpg", "")


settings = Settings()
