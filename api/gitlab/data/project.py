import mongoengine
from urllib.parse import urlparse
from gitlab.data import init_db

from __init__ import init_db

class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=True)
    description = mongoengine.StringField(max_length=100)
    name = mongoengine.StringField(max_length=100)
    web_url = mongoengine.URLField()
    branches = mongoengine.ListField()
    id = mongoengine.StringField(max_length=100)
    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'project'
    }

    def create_project(self, user, description, name, web_url, branches):
        self.user_id = user.id
        self.description = description
        self.name = name
        self.web_url = web_url
        self.branches = branches

        self.save()
        return self
