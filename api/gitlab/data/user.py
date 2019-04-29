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
        user = User()
        user.username = username
        user.save()
        return user


    def get_user(self, username: str):
        user = User.objects(username=username).first()
        return user


    def add_project_user(self, project: Project, user):
        user.project = project
        user.save()
        return user
