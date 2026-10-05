import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "LaptopCare AI"
    API_V1_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./laptopcare.db"
    SECRET_KEY: str = os.environ.get("LAPTOPCARE_SECRET_KEY", "dev-secret-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    MODEL_PATH: str = os.path.join(os.path.dirname(__file__), "..", "ml", "model.joblib")
    LOW_CONFIDENCE_THRESHOLD: float = 0.55
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
