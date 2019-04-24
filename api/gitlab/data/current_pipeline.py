import mongoengine


class CurrentPipeline(mongoengine.Document):
    pipeline_id = mongoengine.ObjectIdField(required=True)
    name = mongoengine.StringField(required=True)

    # jobs = mongoengine.??

    meta = {
        'db_alias': 'ada_GitLab',
        'collection': 'current_pipeline'
    }
