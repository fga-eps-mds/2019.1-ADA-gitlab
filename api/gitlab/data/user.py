import mongoengine
from __init__ import init_db
from project import Project


class User(mongoengine.Document):
    init_db()
    username = mongoengine.StringField(max_length=100)
    project = mongoengine.ReferenceField(Project)
    project_id = mongoengine.StringField(max_length=100)
    gitlab_user = mongoengine.StringField(max_length=100)
    chat_id = mongoengine.StringField(max_length=100)
    gitlab_user_id = mongoengine.StringField(max_length=100)
    project_name = mongoengine.StringField(max_length=100)


    meta = {
        'db_alias': 'AdaBot',
        'collection': 'User'
    }

    def create_user(self, username: str):
        self.username = username
        self.save()
        return self


    def get_user(self, username: str):
        user = User.objects(username=username).first()
        return user

    def save_gitlab_user_data(self, user, gitlab_user, chat_id, gitlab_user_id):
        user.gitlab_user = gitlab_user
        user.chat_id = chat_id
        user.gitlab_user_id = gitlab_user_id
        user.save()
        return user

    def save_gitlab_repo_data(self, user, project_name, project_id):
        user.project_name = project_name
        user.project_id = project_id
        user.update(project_id=project_id, project_name=project_name)
        return user
    
    def add_project_user(self, project):
        self.project = project
        self.save()
        return self
