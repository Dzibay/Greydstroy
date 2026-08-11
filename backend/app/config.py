from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Greydstroy API"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "greydstroy"
    db_user: str = "greydstroy"
    db_password: str = "greydstroy"

    # Пароль входа в админку (обязателен, задаётся в backend/.env)
    admin_password: str = ""
    # Секрет подписи токенов сессии админки (случайная строка)
    admin_token_secret: str = ""
    admin_token_ttl_hours: int = 12

    @property
    def dsn(self) -> str:
        return (
            f"host={self.db_host} port={self.db_port} dbname={self.db_name} "
            f"user={self.db_user} password={self.db_password}"
        )


settings = Settings()
