import os


class Config:
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///simpai.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),  # Reduced from 20
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),  # Reduced from 40
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "10")),  # Reduced from 30
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
        "echo": False,  # Disable SQL logging for performance
        "pool_use_lifo": True,  # Use LIFO for better connection reuse
    }

    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "60"))
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "300 per minute")

    QUIZ_IDEMPOTENCY_TTL_SECONDS = int(os.getenv("QUIZ_IDEMPOTENCY_TTL_SECONDS", "120"))
    AI_TIMEOUT_SECONDS = int(os.getenv("AI_TIMEOUT_SECONDS", "5"))  # Reduced from 8
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(1024 * 1024)))  # 1MB default

    # Query limits
    MAX_QUERY_RESULTS = int(os.getenv("MAX_QUERY_RESULTS", "100"))
    LEADERBOARD_LIMIT = int(os.getenv("LEADERBOARD_LIMIT", "50"))
