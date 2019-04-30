import unittest
from mongoengine import *
from gitlab.data import init_db
from gitlab.data.user import User
from gitlab.data.project import Project

class Test(unittest.TestCase):

    def setup(self):
        init_db()
        Project.drop_collection()
        User.drop_collection()

    def test_create_project(self):
        project = Project()
        description = "Test project"
        name = "Test Project"
        web_url = "https://cakaca.com"
        branches = ["branch1", "branch2"]

        user = User()
        user.username = "User test create project"
        user.save()

        project.create_project(user, description, name, web_url, branches)
        project2 = Project.objects(name = name).first()
        self.assertEquals(project, project2)
        

