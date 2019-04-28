import mongoengine
from gitlab.data import init_db
from gitlab.data.project import Project


class User(mongoengine.Document):
    username = mongoengine.StringField(required=True)
    project_id = mongoengine.StringField(mongoengine.ObjectIdField)

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'User'
    }

    def create_user(self, username: str):
        user = User()
        user.username = username
        user.save()
        return user


    def get_user(self, username: str):
        user = User.objects(username=username).first()
        return user


    def add_project_user(self, project: Project, user: User):
        user.project_id.append(project.id)
        user.save()
        return user
