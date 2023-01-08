from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    chat_id: SecretStr
    db: SecretStr
    api_url: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

