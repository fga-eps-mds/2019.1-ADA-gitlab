import mongoengine
from gitlab.data import init_db
from gitlab.data.project import Project


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
        'db_alias': 'AdaBot',
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
        self.update(project=project)
        return self

    def get_user_project(self):
        project = self.project
        project = Project.objects(id=project.id).first()
        return project
