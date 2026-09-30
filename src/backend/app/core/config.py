from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str

    ALGORITHM: str
    EXPIRY_MINUTES: int
    SECRET_KEY: str

    APP_NAME: str = "CampusOS"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    CORS_ORIGINS: str = "http://localhost:5173"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM_NAME: str = "CampusOS"
    EMAIL_FROM_ADDRESS: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

settings = Settings()