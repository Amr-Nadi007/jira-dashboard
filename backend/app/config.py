"""Application configuration."""
import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Jira Configuration
    jira_url: str = Field(default="", env="JIRA_URL")
    jira_email: str = Field(default="", env="JIRA_EMAIL")
    jira_api_token: str = Field(default="", env="JIRA_API_TOKEN")
    
    # Database
    database_url: str = Field(default="sqlite:///./data/database.db", env="DATABASE_URL")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    
    # Debug
    debug: bool = Field(default=False, env="DEBUG")
    
    # API
    api_title: str = "Jira Dashboard API"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
