import mongoengine
from user import User
from gitlab.data import init_db


class Project(mongoengine.Document):
    user_id = mongoengine.ObjectIdField(required=True)
    description = mongoengine.StringField
    name = mongoengine.StringField
    web_url = mongoengine.URLField
    branches = mongoengine.ListField

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'project'
    }


user_test_for_project = User()
user_test_for_project.username = "test_pipeline_user"
user_test_for_project.save()

project_test = Project()
project_test.user_id = user_test_for_project.id
project_test.name = "Project Test"
project_test.save()

print(project_test.user_id)
