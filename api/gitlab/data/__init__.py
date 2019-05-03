import mongoengine
import os


def init_db():
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_URL = os.environ.get("DB_URL", "")
    mongoengine.connect(DB_NAME, host=DB_URL, alias='AdaBot')
