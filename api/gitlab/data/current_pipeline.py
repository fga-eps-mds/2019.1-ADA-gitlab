import mongoengine
from gitlab.data import init_db
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

    def create_current_pipeline(self, name, jobs, project):
        self.name = name
        self.jobs = jobs
        self.project = project

        self.save()
        return self

    @staticmethod
    def get_current_pipeline(project):
        current_pipeline = CurrentPipeline.\
            objects(project=project).all()

        return current_pipeline
