import mongoengine
from gitlab.data import init_db


class CurrentPipeline(mongoengine.Document):
    #pipeline_id = mongoengine.ObjectIdField(required=True)
    name = mongoengine.StringField(required=True)
    jobs = mongoengine.ListField(mongoengine.DictField())

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'CurrentPipeline'
    }

    def clean(self):
        jobs = self.jobs

        for job in jobs:
            if not job['duration']:
                raise ValidationError('Duration of pipeline not defined')
            if not job['date']:
                raise ValidationError('date of pipeline not defined')
            if not job['name']:
                raise ValidationError('name of pipeline not defined')
            if not job['stage']:
                raise ValidationError('stage of pipeline not defined')
            if not job['status']:
                raise ValidationError('status of pipeline not defined')
            if not job['web_url']:
                raise ValidationError('Web Url of pipeline not defined')
