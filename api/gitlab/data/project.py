import mongoengine
from gitlab.data import init_db


class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=True)
    description = mongoengine.StringField(max_length=100)
    name = mongoengine.StringField(max_length=100)
    web_url = mongoengine.URLField()
    branches = mongoengine.ListField()
    project_id = mongoengine.StringField(max_length=100)
    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'Project'
    }

    def create_project(self, user, description, name,
                       web_url, branches, project_id):
        self.user_id = user.id
        self.description = description
        self.name = name
        self.web_url = web_url
        self.branches = branches
        self.project_id = project_id
        self.save()
        return self

    def save_webhook_infos(self, user, name, project_id):
        self.user_id = user.id
        self.name = name
        self.project_id = project_id
        self.save()
        return self
