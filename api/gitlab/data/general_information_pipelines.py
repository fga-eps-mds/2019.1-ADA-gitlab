import mongoengine
from __init__ import init_db
from project import Project

class GeneralInformationPipelines(mongoengine.Document):
    project = mongoengine.ReferenceField(Project, required=True)
    number_of_pipelines = mongoengine.IntField
    successful_pipelines = mongoengine.IntField

    init_db()
    meta = {
        'db_alias': 'AdaBot',
        'collection': 'Pipeline'
    }

    def create_general_information_pipeline(self, project: Project, number_of_pipelines: int, successful_pipelines: int):
        pipeline = GeneralInformationPipelines()
        pipeline.project = project
        pipeline.number_of_pipelines = number_of_pipelines
        pipeline.successful_pipelines = successful_pipelines

        pipeline.save()
        return pipeline

    @staticmethod
    def get_general_information_pipeline(self, project: Project):
        general_information_pipeline = GeneralInformationPipelines.objects(
            project=project).first()
        return general_information_pipeline


    def add_pipeline(self, pipeline, project: Project):
        general_information_pipeline = self.get_general_information_pipeline(project)
        general_information_pipeline.modify(upsert=True, new=True, inc__number_of_pipelines=1)
        all_jobs_successful = True
        for job in pipeline.jobs:
            if not job['status']:
                all_jobs_successful = False
                break
            else:
                # do nothing, if job status is true then it is successful
                continue
        if all_jobs_successful:
            general_information_pipeline.modify(upsert=True, new=True, inc__successful_pipelines=1)
        else:
            # do nothing, if pipeline fails, only the number of pipelines increases
            pass
