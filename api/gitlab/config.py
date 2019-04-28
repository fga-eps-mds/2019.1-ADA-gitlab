# api/gitlab/config.py
import os


class BaseConfig:
    """Base configuration"""
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    MONGODB_SETTINGS = {
        "db": os.environ.get("DB_NAME", ""),
        "host": os.environ.get("DB_NAME", "")
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    """Production configuration"""
    MONGO_DATABASE_URI = os.environ.get("DATABASE_URL")
