from gitlab.tests.base import BaseTestCase
from gitlab.data.user import User
from gitlab.data.project import Project
from gitlab.data.general_information_pipelines import \
    GeneralInformationPipelines
from gitlab.data.current_pipeline import CurrentPipeline


class Test(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_create_current_pipeline(self):
        CurrentPipeline.drop_collection()
        Project.drop_collection()
        User.drop_collection()

        user = User()
        user.username = "User test current pipeline"
        user.save()

        project = Project()
        project.user_id = user.id
        project.description = "Test project current pipeline"
        project.name = "Test project current pipeline"
        project.web_url = "https://currentpipeline.com"
        project.branches = ["branch1", "branch2"]
        project.save()

        current_pipeline = CurrentPipeline()
        name = "Test current"
        pipeline_jobs = [{"Teste": "Testando"}]
        current_pipeline.create_current_pipeline(name, pipeline_jobs, project)

        current_pipeline2 = CurrentPipeline.objects(name=name).first()

        self.assertEqual(current_pipeline, current_pipeline2)

    def test_get_current_pipeline(self):
        CurrentPipeline.drop_collection()
        Project.drop_collection()
        User.drop_collection()

        user = User()
        user.username = "User test current pipeline"
        user.save()

        project = Project()
        project.user_id = user.id
        project.description = "Test project current pipeline"
        project.name = "Test project current pipeline"
        project.web_url = "https://currentpipeline.com"
        project.branches = ["branch1", "branch2"]
        project.save()

        currentpipeline = CurrentPipeline()
        currentpipeline.project = project
        currentpipeline.name = "Test current"
        currentpipeline.pipeline_jobs = [{"Teste": "Testando"}]
        currentpipeline.save()

        generalinfo = GeneralInformationPipelines()
        generalinfo.project = project
        generalinfo.number_of_pipelines = 10
        generalinfo.successful_pipelines = 5
        generalinfo.save()

        pipelines_in_db = CurrentPipeline.get_current_pipeline(project)
        for pipeline in pipelines_in_db:
            self.assertEqual(currentpipeline, pipeline)
