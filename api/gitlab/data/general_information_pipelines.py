import mongoengine
from mongo_setup import global_init


class GeneralInformationPipelines(mongoengine.Document):
    project_id = mongoengine.ObjectIdField(required=True)
    number_of_pipelines = mongoengine.IntField
    successful_pipelines = mongoengine.IntField

    global_init()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'Pipeline'
    }
