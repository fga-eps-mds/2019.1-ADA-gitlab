import mongoengine
from __init__ import init_db
from project import Project


class User(mongoengine.Document):
    username = mongoengine.StringField(required=True)
    project = mongoengine.ReferenceField(Project)

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'User'
    }

    def create_user(self, username: str):
        self.username = username
        self.save()
        return self

    def add_project_user(self, project: Project):
        self.project = project
        self.save()
        return self
