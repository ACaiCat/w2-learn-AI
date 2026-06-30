from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_NAME: str = "glm-5.1"
    API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env"
    )

def get_settings(): return Settings()