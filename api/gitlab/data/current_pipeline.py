import mongoengine
from __init__ import init_db
from general_information_pipelines import GeneralInformationPipelines
from project import Project

class CurrentPipeline(mongoengine.Document):
    project = mongoengine.ReferenceField(Project, required=True)
    name = mongoengine.StringField(required=True)
    jobs = mongoengine.ListField(mongoengine.DictField())

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'CurrentPipeline'
    }

    def create_current_pipeline(self, name: str, jobs: list, project: Project):
        current_pipeline = CurrentPipeline()
        current_pipeline.name = name
        current_pipeline.jobs = jobs
        current_pipeline.project = project

        current_pipeline.save()
        return current_pipeline

    def get_current_pipeline(self, project: Project):
        pipeline = GeneralInformationPipelines.get_general_information_pipeline(project)
        current_pipeline = CurrentPipeline.objects(pipeline_id=pipeline.id).all()

        return current_pipeline
