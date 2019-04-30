import unittest
from mongoengine import *
from gitlab.data.user import User
from gitlab.data import init_db

class Test(unittest.TestCase):
    
    def setup(self):
        init_db()
        User.drop_collection()


    def test_create_user(self):
        User.drop_collection()
        user = User()
        username = "teste_User"
        user.create_user(username)
        #User.drop_collection()
        

        user2 = User.objects(username = username).first()
        self.assertEqual(user, user2)


