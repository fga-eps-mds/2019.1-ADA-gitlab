import mongoengine
from urllib.parse import urlparse
from user import User
from gitlab.data import init_db
from gitlab.data.user import User


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

    def create_project(self, user: User, description: str, name: str, web_url: str, branches: list) -> Project:
        project = Project()
        project.user_id = user.id
        project.description = description
        project.name = name
        project.web_url = web_url
        project.branches = branches

        project.save()

        user = User()
        user.add_project_user(project, user)
        return project


    def get_project(self, name: str) -> Project:
        project = Project.objects(name=name).first()
        return project
    
    def clean_jobs(self):
        pass


# user_test_for_project = User()
# user_test_for_project.username = "test_pipeline_user"
# user_test_for_project.save()

# project_test = Project()
# project_test.user_id = user_test_for_project.id
# project_test.name = "Project Test"
# project_test.save()

# print(project_test.user_id)
