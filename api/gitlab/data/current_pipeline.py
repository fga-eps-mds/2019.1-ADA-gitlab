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

    def clean(self):
        keys = {'duration': 'double',
                'date': 'str',
                'name': 'str',
                'stage': 'str',
                'status': 'bool',
                'web_url': 'str'}
        for job in pipeline_jobs:
            if list(keys.keys()) == list(job.keys()):
                # everything is okay is job has all keys
                pass
            else:
                raise ValidationError('O job não possui todas as informações')
            for key in keys:
                if '<class \'' + keys[key] + '\'>' == str(type(job[key])):
                    # everything okay
                    pass
                else:
                    raise ValidationError('Os dados salvos são '
                                          + 'incompatíveis com a estrutura')


    def create_current_pipeline(self, name: str, jobs: list, project: Project):
        self.name = name
        self.jobs = jobs
        self.project = project

        self.save()
        return self

    @staticmethod
    def get_current_pipeline(project: Project):
        current_pipeline = CurrentPipeline.\
            objects(project=project).all()

        return current_pipeline
