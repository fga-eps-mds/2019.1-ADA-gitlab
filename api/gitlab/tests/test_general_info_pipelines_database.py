from gitlab.data import init_db
from gitlab.tests.base import BaseTestCase
from gitlab.data.project import Project
from gitlab.data.user import User
from gitlab.data.current_pipeline import CurrentPipeline
from gitlab.data.general_information_pipelines import \
    GeneralInformationPipelines


class TestGeneralInformationPipeline(BaseTestCase):

    def setUp(self):
        super().setUp()
        GeneralInformationPipelines.drop_collection()
        Project.drop_collection()
        self.user = User()
        self.user.username = "User test create project"
        self.user.save()

        self.project = Project()
        self.project.user_id = self.user.id
        self.project.description = "Test project current pipeline"
        self.project.name = "Test project current pipeline"
        self.project.web_url = "https://currentpipeline.com"
        self.project.branches = ["branch1", "branch2"]
        self.project.save()

        self.general_information_pipeline = GeneralInformationPipelines()
        self.number_of_pipelines = 10
        self.successful_pipelines = 5
        self.general_information_pipeline.create_general_information_pipeline(
            self.project, self.number_of_pipelines, self.successful_pipelines)

    def test_create_general_information_pipeline(self):
        general_info_db = GeneralInformationPipelines.objects(
            project=self.project).first()
        self.assertEqual(self.general_information_pipeline, general_info_db)

    def get_test_general_information_pipeline(self):
        general_info = GeneralInformationPipelines.\
            get_general_information_pipeline(self.project)
        self.assertEqual(self.general_information_pipeline, general_info)

    def test_add_pipeline_fail(self):
        current_pipeline = CurrentPipeline()
        name = "Test current2"
        pipeline_jobs = [{"duration": 9.8,
                          'date': '03/04/2019',
                          'name': 'nome',
                          'stage': 'flake8',
                          'status': False,
                          'web_url': 'http://teste.com'}]
        current_pipeline.create_current_pipeline(name,
                                                 pipeline_jobs, self.project)

        self.general_information_pipeline.add_pipeline(current_pipeline,
                                                       self.project)
        general_info = GeneralInformationPipelines.\
            get_general_information_pipeline(self.project)
        self.assertEqual(self.number_of_pipelines + 1,
                         general_info.number_of_pipelines)
        self.assertEqual(self.successful_pipelines,
                         general_info.successful_pipelines)

    def test_add_pipeline_sucess(self):
        current_pipeline = CurrentPipeline()
        name = "Test current"
        pipeline_jobs = [{'duration': 9.8,
                          'date': '03/04/2019',
                          'name': 'nome',
                          'stage': 'flake8',
                          'status': True,
                          'web_url': 'http://teste.com'}]
        current_pipeline.create_current_pipeline(name,
                                                 pipeline_jobs, self.project)

        self.general_information_pipeline.add_pipeline(current_pipeline,
                                                       self.project)
        general_info = GeneralInformationPipelines.\
            get_general_information_pipeline(self.project)
        self.assertEqual(self.number_of_pipelines + 1,
                         general_info.number_of_pipelines)
        self.assertEqual(self.successful_pipelines + 1,
                         general_info.successful_pipelines)
