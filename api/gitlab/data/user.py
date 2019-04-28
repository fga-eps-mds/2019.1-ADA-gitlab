import mongoengine
from gitlab.data import init_db



class User(mongoengine.Document):
    username = mongoengine.StringField(required=True)

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'User'
    }


user_test = User()
user_test.username = "Caio_User_Test"
user_test.save()
