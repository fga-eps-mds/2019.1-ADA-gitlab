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

    def get_commits(self, project_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "repository/commits"\
              .format(project_id=project_id)
        repo_commits = self.get_request(url)
        number_of_commits = len(repo_commits)
        self.update_commits_data(repo_commits, number_of_commits)
    
    def update_commits_data(self, repo_commits, number_of_commits):
        commit_statistics = self.repo["commits"]["last_commit"]
        for key in self.repo["commits"]["last_commit"]:
            commit_statistics[key] = repo_commits[0][key]
        (self.repo["commits"]
                  ["number_of_commits"]) = number_of_commits