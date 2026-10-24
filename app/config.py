from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    agency_data_path: str = "data/agency_records.json"
    payment_data_path: str = "data/payments.json"
    output_dir: str = "output"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

settings = Settings()
