import mongoengine


class Pipeline(mongoengine.Document):
    project_id = mongoengine.ObjectIdField(required=True)
    current_pipeline_name = mongoengine.StringField
    failed_pipelines = mongoengine.IntField
    number_of_pipelines = mongoengine.IntField
    percentage_success = mongoengine.IntField
    successful_pipelines = mongoengine.IntField

    meta = {
        'db_alias': 'ada_GitLab',
        'collection': 'pipeline'
    }
