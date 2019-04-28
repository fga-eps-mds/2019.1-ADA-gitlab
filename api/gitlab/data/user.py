import mongoengine
from mongo_setup import global_init


class User(mongoengine.Document):
    username = mongoengine.StringField(required=True)
    project_id = mongoengine.ListField(mongoengine.ObjectIdField)

    global_init()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'User'
    }


user_test = User()
user_test.username = "Caio_User_Test"
user_test.save()
