from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    database_url: str = "sqlite:///./tmp/pydev1.db"
    database_debug: bool = True

    openapi_json:  str | None = "/api/openapi.json"
    openapi_docs:  str | None = "/api-docs"
    openapi_redoc: str | None = "/api-redoc"

    class Config:
        env_file = ".env"


conf = Settings()
