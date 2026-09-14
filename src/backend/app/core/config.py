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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()