import mongoengine
from jobs_embedded import JobEmbedded
from mongo_setup import global_init


class CurrentPipeline(mongoengine.Document):
    #pipeline_id = mongoengine.ObjectIdField(required=True)
    name = mongoengine.StringField(required=True)
    jobs = mongoengine.DictField()

    global_init()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'owners'
    }


test = CurrentPipeline()
test.name = "Caio"
test.save()

print(test.name)
