import requests
from requests.exceptions import HTTPError
import json
from datetime import date
from datetime import datetime


class Report():
    pipelines_ids = []

    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
        self.repo = {
                          "branches": {
                            "name": 0
                          },
                          "commits": {
                              "last_commit": {
                                  "title": 0,
                                  "author_name": 0,
                                  "author_email": 0,
                                  "authored_date": 0
                              },
                              "number_of_commits": 0
                          },
                          "project": {
                              "name": 0,
                              "web_url": 0
                          },
                          "pipelines": {
                              "number_of_pipelines": 0,
                              "succeded_pipelines": 0,
                              "failed_pipelines": 0,
                              "percent_succeded": 0,
                              "current_pipeline_id": 0,
                              "current_pipeline_name": 0,
                              "recents_pipelines": {
                                  "last_7_days": {
                                      "number_of_pipelines": 0,
                                      "percent_succeded": 0,
                                      "percent_failed": 0,
                                      "succeded_pipelines": 0,
                                      "failed_pipelines": 0
                                  },
                                  "last_30_days": {
                                      "number_of_pipelines": 0,
                                      "percent_succeded": 0,
                                      "percent_failed": 0,
                                      "succeded_pipelines": 0,
                                      "failed_pipelines": 0
                                  }
                                }
                          },
                          "pipelines_times": {
                              "average": 0,
                              "lower": 0,
                              "higher": 0,
                              "total": 0
                          }
                        }

    def get_branches(self, project_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/"
                                    "repository/branches"
                                    .format(project_id=project_id),
                                    headers=headers)
            branches_json = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            branch_name = {"name": []}
            for i, item in enumerate(branches_json):
                branch_name["name"].append(branches_json[i]["name"])
            self.repo["branches"]["name"] = branch_name["name"]

    def get_commits(self, project_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }

        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/"
                                    "repository/commits"
                                    .format(project_id=project_id),
                                    headers=headers)
            commit = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            number_of_commits = len(commit)
            (self.repo["commits"]
                      ["last_commit"]
                      ["title"]) = commit[0]["title"]
            (self.repo["commits"]
                      ["last_commit"]
                      ["author_name"]) = commit[0]["author_name"]
            (self.repo["commits"]
                      ["last_commit"]
                      ["author_email"]) = commit[0]["author_email"]
            (self.repo["commits"]
                      ["last_commit"]
                      ["authored_date"]) = commit[0]["authored_date"]
            (self.repo["commits"]
                      ["number_of_commits"]) = number_of_commits

    def get_project(self, project_owner, project_name):
        self.repo["project"]["name"] = project_name
        url = "https://gitlab.com/"+project_owner+'/'+project_name
        self.repo["project"]["web_url"] = url

    def get_pipeline(self, project_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/"
                                    "{project_id}/pipelines"
                                    .format(project_id=project_id),
                                    headers=headers)
            pipelines = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            number_of_pipelines = 0
            success_pipeline = 0
            failed_pipeline = 0

            last_7_days = [0, 0, 0, 0, 0]
            last_30_days = [0, 0, 0, 0, 0]
            for i, item in enumerate(pipelines):
                self.pipelines_ids.append(pipelines[i]["id"])
                is_recent = self.check_pipeline_date(
                    project_id, pipelines[i]["id"])
                if is_recent[0]:
                    if is_recent[1] == 7:
                        last_7_days[0] += 1
                        if pipelines[i]["status"] == "success":
                            last_7_days[1] += 1
                        else:
                            last_7_days[2] += 1
                    else:
                        last_30_days[0] += 1
                        if pipelines[i]["status"] == "success":
                            last_30_days[1] += 1
                        else:
                            last_30_days[2] += 1

                if pipelines[i]["status"] == "success":
                    success_pipeline = success_pipeline + 1
                else:
                    failed_pipeline = failed_pipeline + 1
            if last_30_days[0]:
                last_30_days[3] = (last_30_days[1]/last_30_days[0]) * 100.0
                last_30_days[4] = 100 - last_30_days[3]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_30_days"]
                      ["number_of_pipelines"]) = last_30_days[0]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_30_days"]
                      ["percent_succeded"]) = last_30_days[3]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_30_days"]
                      ["percent_failed"]) = last_30_days[4]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_30_days"]
                      ["succeded_pipelines"]) = last_30_days[1]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_30_days"]
                      ["failed_pipelines"]) = last_30_days[2]

            if last_7_days[0]:
                last_7_days[3] = (last_7_days[1]/last_7_days[0])*100.0
                last_7_days[4] = 100 - last_7_days[3]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_7_days"]
                      ["number_of_pipelines"]) = last_7_days[0]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_7_days"]
                      ["percent_succeded"]) = last_7_days[3]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_7_days"]
                      ["percent_failed"]) = last_7_days[4]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_7_days"]
                      ["succeded_pipelines"]) = last_7_days[1]
            (self.repo["pipelines"]
                      ["recents_pipelines"]
                      ["last_7_days"]
                      ["failed_pipelines"]) = last_7_days[2]

            number_of_pipelines = len(pipelines)
            percent_success = (success_pipeline / number_of_pipelines) * 100.0
            (self.repo["pipelines"]
                      ["number_of_pipelines"]) = number_of_pipelines
            (self.repo["pipelines"]
                      ["succeded_pipelines"]) = success_pipeline
            (self.repo["pipelines"]
                      ["failed_pipelines"]) = failed_pipeline
            (self.repo["pipelines"]
                      ["percent_succeded"]) = percent_success
            (self.repo["pipelines"]
                      ["current_pipeline_id"]) = pipelines[0]["id"]
            (self.repo["pipelines"]
                      ["current_pipeline_name"]) = pipelines[0]["ref"]

    def check_pipeline_date(self, project_id, pipeline_id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/"
                                    "{project_id}/pipelines/{pipeline_id}"
                                    .format(project_id=project_id,
                                            pipeline_id=pipeline_id),
                                    headers=headers)
            pipeline = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            todays_date = date.today()
            pipeline_date = datetime.strptime(
                pipeline['created_at'][0:10], "%Y-%m-%d")
            pipeline_date = pipeline_date.date()
            qntd_days = todays_date-pipeline_date

            if(qntd_days.days <= 7):
                return [True, 7]
            elif(qntd_days.days <= 30):
                return [True, 30]
            return [False]

    def repo_informations(self, user, project):
        project_id = int(project.project_id)
        project_name = project.name
        project_owner = user.gitlab_user
        self.get_branches(project_id)
        self.get_commits(project_id)
        self.get_project(project_owner, project_name)
        self.get_pipeline(project_id)
        generated_report = []
        generated_report.append(self.repo)
        return generated_report
