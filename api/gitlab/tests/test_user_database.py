import unittest
from mongoengine import *
from gitlab.data.user import User
from gitlab.data import init_db
from gitlab.data.project import Project

class Test(unittest.TestCase):
    
    def setup(self):
        init_db()
        User.drop_collection()
        Project.drop_collection()


    def test_create_user(self):
        User.drop_collection()
        user = User()
        username = "teste_User"
        user.create_user(username)
        #User.drop_collection()
        
        user2 = User.objects(username = username).first()
        self.assertEqual(user, user2)

    def test_add_project_user(self):
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

        user.add_project_user(project)
        

        project_user = User.objects(project = project).first()
        self.assertEqual(user, project_user)
        
        





