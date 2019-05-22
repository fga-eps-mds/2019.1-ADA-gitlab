import requests
from requests.exceptions import HTTPError
import json
from datetime import date
from datetime import datetime
from gitlab.report.report_json import report_dict
from gitlab.utils.gitlab_utils import GitlabUtils
import sys


class ReportCommits(GitlabUtils):
    def __init__(self, GITLAB_API_TOKEN):
        super().__init__(GITLAB_API_TOKEN)
        self.repo = report_dict
    
    pipelines_ids = []    

    def get_commits(self, project_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "repository/commits"\
              .format(project_id=project_id)
        repo_commits = self.get_request(url)
        number_of_commits = len(repo_commits)
        (self.repo["commits"]
                    ["last_commit"]
                    ["title"]) = repo_commits[0]["title"]
        (self.repo["commits"]
                    ["last_commit"]
                    ["author_name"]) = repo_commits[0]["author_name"]
        (self.repo["commits"]
                    ["last_commit"]
                    ["author_email"]) = repo_commits[0]["author_email"]
        (self.repo["commits"]
                    ["last_commit"]
                    ["authored_date"]) = repo_commits[0]["authored_date"]
        (self.repo["commits"]
                    ["number_of_commits"]) = number_of_commits