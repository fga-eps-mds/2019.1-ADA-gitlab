import requests
from requests.exceptions import HTTPError
import json
from datetime import date
from datetime import datetime
from gitlab.report.report_json import report_dict
from gitlab.utils.gitlab_utils import GitlabUtils
from gitlab.report.branch_utils import ReportBranches
from gitlab.report.commit_utils import ReportCommits
from gitlab.report.pipeline_report_utils \
     import ReportPipelines
import sys

class Report(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.repo = report_dict    

    def get_project(self, project_owner, project_name):
        self.repo["project"]["name"] = project_name
        url = "https://gitlab.com/"+project_owner+'/'+project_name
        self.repo["project"]["web_url"] = url

    def repo_informations(self, user, project):
        project_id = int(project.project_id)
        project_name = project.name
        project_owner = user.gitlab_user
        branches = ReportBranches(self.chat_id)
        commits = ReportCommits(self.chat_id)
        pipelines = ReportPipelines(self.chat_id)
        branches.get_branches(project_id) 
        commits.get_commits(project_id)
        self.get_project(project_owner, project_name)
        pipelines.get_pipeline(project_id)
        generated_report = []
        generated_report.append(self.repo)
        return generated_report
