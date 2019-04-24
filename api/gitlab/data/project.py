import mongoengine


class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=True)
    description = mongoengine.StringField
    name = mongoengine.StringField
    web_url = mongoengine.URLField
    branches = mongoengine.ListField

    meta = {
        'db_alias': 'ada_GitLab',
        'collection': 'project'
    }
