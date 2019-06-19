import mongoengine
import os


def init_db():
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_URL = os.environ.get("DB_URL", "")
    db = mongoengine.connect(DB_NAME, host=DB_URL,
                             alias='AdaCronjob')
    return db


class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=True)
    description = mongoengine.StringField(max_length=100)
    name = mongoengine.StringField(max_length=100)
    web_url = mongoengine.URLField()
    branches = mongoengine.ListField()
    project_id = mongoengine.StringField(max_length=100)
    init_db()
    meta = {
        'db_alias': 'AdaCronjob',
        'collection': 'Project'
    }

    def save_webhook_infos(self, user, name, project_id):
        self.user_id = user.id
        self.name = name
        self.project_id = project_id
        self.save()
        return self
