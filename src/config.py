import logging
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    app_name: str = "API Documentation AI Assistant"
    app_description: str = "AI-powered API documentation assistant"
    app_version: str = "0.0.1"
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()
