# api/gitlab/config.py
import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    MONGODB_SETTINGS = {
        'db': 'api',
        'host': 'mongodb://mongo-gitlab:27010/api'
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    MONGO_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    MONGO_DATABASE_URI = os.environ.get('DATABASE_URL')
