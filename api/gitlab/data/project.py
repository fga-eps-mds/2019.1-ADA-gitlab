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

    def save_webhook_infos(self, user, name, project_id):
        self.user_id = user.id
        self.name = name
        self.project_id = project_id
        self.save()
        return self

    def update_webhook_infos(self, name, project_id):
        self.name = name
        self.project_id = project_id
        self.update(name=name, project_id=project_id)
        return self
