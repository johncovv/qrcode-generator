from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "production"

    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = ""
    aws_s3_bucket_name: str = ""

    class Config:
        env_file = ".env"

    @property
    def is_development(self) -> bool:
        return self.environment.lower() != "production"


settings = Settings()
