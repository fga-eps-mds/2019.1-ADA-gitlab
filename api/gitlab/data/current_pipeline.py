import mongoengine
from gitlab.data import init_db
from gitlab.data.general_information_pipelines import GeneralInformationPipelines
from gitlab.data.project import Project

class CurrentPipeline(mongoengine.Document):
    project_id = mongoengine.ObjectIdField(required=True)
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
        current_pipeline.project_id = project.id

        current_pipeline.save()
        return current_pipeline

    def get_current_pipeline(self, project: Project):
        pipeline = GeneralInformationPipelines.get_general_information_pipeline(project)
        current_pipeline = CurrentPipeline.objects(pipeline_id=pipeline.id).all()

        return current_pipeline
