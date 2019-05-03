from gitlab.data.user import User
from gitlab.data import init_db
from gitlab.data.project import Project
from gitlab.tests.base import BaseTestCase


class Test(BaseTestCase):

    def setup(self):
        init_db()
        User.drop_collection()
        Project.drop_collection()

    def test_create_user(self):
        User.drop_collection()
        user = User()
        username = "teste_User"
        user.create_user(username)

        user2 = User.objects(username=username).first()
        self.assertEqual(user, user2)

    def test_save_gitlab_repo_data(self):
        User.drop_collection()
        user = User()
        username = "teste_User"
        user.create_user(username)
        user.save()

        Project.drop_collection()
        project = Project()
        project.user_id = user.id
        project.description = "Test user add project"
        project.name = "Test user add project"
        project.web_url = "https://useraddProject.com"
        project.branches = ["branch1", "branch2"]
        project.save()

        user.save_gitlab_repo_data(project)

        project_user = User.objects(project=project).first()
        self.assertEqual(user, project_user)

    def test_save_gitlab_user_data(self):
        gitlab_user = 'git_user'
        chat_id = 'id'
        gitlab_user_id = 'git_id'
        username = 'nomeee'
        user = User()
        user.username = username
        user.save()
        user.save_gitlab_user_data(gitlab_user, chat_id, gitlab_user_id)

        user_db = User.objects(username=username).first()
        self.assertEqual(user, user_db)
