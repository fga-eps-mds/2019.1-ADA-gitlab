import mongoengine
from project import Project
import os


def init_db():
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_URL = os.environ.get("DB_URL", "")
    db = mongoengine.connect(DB_NAME, host=DB_URL,
                             alias='AdaCronjob')
    return db


class User(mongoengine.Document):
    init_db()
    username = mongoengine.StringField(max_length=100)
    project = mongoengine.ReferenceField(Project)
    access_token = mongoengine.StringField(max_length=100)
    gitlab_user = mongoengine.StringField(max_length=100)
    chat_id = mongoengine.StringField(max_length=100)
    gitlab_user_id = mongoengine.StringField(max_length=100)
    api_token = mongoengine.StringField(max_length=100)
    domain = mongoengine.URLField()
    meta = {
        'db_alias': 'AdaCronjob',
        'collection': 'User'
    }

    def create_user(self, username):
        self.username = username
        self.save()
        return self

    def save_gitlab_user_data(self, gitlab_user,
                              chat_id, gitlab_user_id):
        self.gitlab_user = gitlab_user
        self.chat_id = chat_id
        self.gitlab_user_id = gitlab_user_id
        self.save()
        return self

    def save_gitlab_repo_data(self, project):
        self.project = project
        self.save()
        return self

    def get_user_project(self):
        project = self.project
        project = Project.objects(id=project.id).first()
        return project
