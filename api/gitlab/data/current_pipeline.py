import mongoengine
from gitlab.data import init_db
from gitlab.data.general_information_pipelines import GeneralInformationPipelines
from gitlab.data.project import Project


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
        self.name = name
        self.jobs = jobs
        self.project = project

        self.save()
        return self

    def get_current_pipeline(self, project: Project):
        pipeline = GeneralInformationPipelines.\
            get_general_information_pipeline(project)
        current_pipeline = CurrentPipeline.\
            objects(pipeline_id=pipeline.id).all()

        return current_pipeline
