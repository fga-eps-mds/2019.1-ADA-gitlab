import mongoengine
from gitlab.data import init_db
from gitlab.data.project import Project
from gitlab.data.pipeline import Pipeline

class GeneralInformationPipelines(mongoengine.Document):
    project_id = mongoengine.ObjectIdField(required=True)
    number_of_pipelines = mongoengine.IntField
    successful_pipelines = mongoengine.IntField

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'Pipeline'
    }

    def create_general_information_pipeline(self, project: Project, number_of_pipelines: int, successful_pipelines: int) -> GeneralInformationPipelines:
        pipeline = GeneralInformationPipelines()
        pipeline.project_id = project.id
        pipeline.number_of_pipelines = number_of_pipelines
        pipeline.successful_pipelines = successful_pipelines

        pipeline.save()
        return pipeline


    def get_general_information_pipeline(self, project: Project) -> GeneralInformationPipelines:
        pipeline = GeneralInformationPipelines.objects(
            project_id=project.id).first()
        return pipeline
