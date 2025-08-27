import os


class Config:
    """Configuration settings for the application"""

    # Server settings
    ENV: str = os.getenv("ENV", "DEV")
    VERSION: str = "1.0.0"
    PORT: int = int(os.getenv("PORT", 7000))

    # Database settings
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT"))
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

    # Auth settings
    SENTINEL_URL: str = os.getenv("SENTINEL_URL")
    SENTINEL_JWKS_URL: str = os.getenv("SENTINEL_JWKS_URL")
    SENTINEL_CLIENT_ID: str = os.getenv("SENTINEL_CLIENT_ID")
    SENTINEL_CLIENT_SECRET: str = os.getenv("SENTINEL_CLIENT_SECRET")
    SENTINEL_TOKEN: str = os.getenv("SENTINEL_TOKEN")
    SENTINEL_REDIRECT_URI: str = os.getenv("SENTINEL_REDIRECT_URI")

    @staticmethod
    def get_database_url() -> str:
        """Constructs the PostgreSQL database URL from individual settings"""
        return f"postgresql+psycopg2://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOST}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}"
