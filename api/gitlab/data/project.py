import mongoengine
from __init__ import init_db


class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=True)
    description = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    web_url = mongoengine.URLField(required=True)
    branches = mongoengine.ListField(required=True)
    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'project'
    }

    def create_project(self, user, description: str,
                       name: str, web_url: str, branches: list):
        self.user_id = user.id
        self.description = description
        self.name = name
        self.web_url = web_url
        self.branches = branches

        self.save()
        return self
