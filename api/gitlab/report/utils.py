import requests
from requests.exceptions import HTTPError
import json
from flask import jsonify
import sys


'''
US30 - Informações para o relatório
Project Resources - https://docs.gitlab.com/ee/api/#project-resources

Nome do repo -> projects [ name ]
Branches
    -Name
Commits
    -Quantidade de commits (como ?)
    -Último commit
        -Title
        -Author_name
        -Author_email
        -Authored_date
Jobs
    -Status
    -Stage
    -Name
    -Ref
    -pipeline
        -Ref
        -Status
        -Web_url
Members from project , not from groups
    -Name
    -Username
    -State
Projects
    -Name
    -Path
    -Description
    -web_url
Pipelines
    -number_of_pipelines --> ok
    -succeded --> ok
    -failed --> ok
    -succeded_percentage --> ok
    -Gráfico de sucesso de pipelines da última semana e último mês (imagem)
Current_pipeline
    -name
    -jobs
        -status 

*** Info necessaria para pegar essas info: id do project
'''

class Report():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
        self.repo_json = {"branches": {"name": 0}, "members": {"name": 0, "username": 0,
                         "state": 0}, "commits": {"last_commit": {"title": 0, "author_name": 0,
                         "author_email": 0, "authored_date": 0}, "number_of_commits": 0},
                          "project": {"description": 0, "name": 0, "web_url": 0},
                          "pipelines":{"number_of_pipelines": 0, "succeded_pipelines": 0,
                          "failed_pipelines": 0, "percent_succeded": 0}}

    def get_branches(self, project_owner, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_id = self.get_project_id(project_owner, project_name)
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/repository/branches"
                                    .format(project_id=project_id["id"]),
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
            self.repo_json["branches"]["name"] = branch_name["name"]

    def get_members(self, project_owner, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }

        project_id = self.get_project_id(project_owner, project_name)
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/{project_id}/members".format(project_id=project_id["id"]), headers=headers)
            members_json = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            data_members = {"name": [], "username": [], "state": []}
            for i, item in enumerate(members_json):
                 data_members["name"].append(members_json[i]["name"])
                 data_members["username"].append(members_json[i]["username"])
                 data_members["state"].append(members_json[i]["state"])
            self.repo_json["members"]["name"] = data_members["name"]
            self.repo_json["members"]["username"] = data_members["username"]
            self.repo_json["members"]["state"] = data_members["state"]

    def get_commits(self, project_owner, project_name):

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }

        project_id = self.get_project_id(project_owner, project_name)
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/{project_id}/repository/commits".format(project_id=
                                     project_id["id"]), headers=headers)
            commits_json = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
                dict_error = {"status_code": http_error.response.status_code}
                raise HTTPError(json.dumps(dict_error))
        else:
            self.repo_json["commits"]["last_commit"]["title"] = commits_json[0]["title"]
            self.repo_json["commits"]["last_commit"]["author_name"] = commits_json[0]["author_name"]
            self.repo_json["commits"]["last_commit"]["author_email"] = commits_json[0]["author_email"]
            self.repo_json["commits"]["last_commit"]["authored_date"] = commits_json[0]["authored_date"]
            number_of_commits = 0

            for i, item in enumerate(commits_json):
                number_of_commits = number_of_commits + 1
            self.repo_json["commits"]["number_of_commits"] = number_of_commits
            # print(self.repo_json, file=sys.stderr)

    def get_jobs(self, project_id, headers):
        pass # quantos jobs vamos pegar ?


    def get_project(self, project_owner, project_name):

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }

        project_id = self.get_project_id(project_owner, project_name)
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/{project_id}".format(project_id=project_id["id"]), headers=headers)
            project_json = response.json()

            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            self.repo_json["project"]["name"] = project_json["name"]
            self.repo_json["project"]["description"] = project_json["description"]
            self.repo_json["project"]["web_url"] = project_json["web_url"]

            # print(self.repo_json, file=sys.stderr)

    def get_pipeline(self, project_owner, project_name):
        # ultima pipeline
        # desempenho do ultimo mes
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_id = self.get_project_id(project_owner, project_name)
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/{project_id}/pipelines".format(project_id=project_id["id"]), headers=headers)
            pipelines = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            number_of_pipelines = 0
            success_pipeline = 0
            failed_pipeline = 0
            for i, item in enumerate(pipelines):
                number_of_pipelines = number_of_pipelines + 1 #total
                if pipelines[i]["status"] == "success":
                    success_pipeline = success_pipeline + 1
                else:
                    failed_pipeline = failed_pipeline + 1
            percent_success = (success_pipeline / number_of_pipelines) * 100.0
            self.repo_json["pipelines"]["number_of_pipelines"] = number_of_pipelines
            self.repo_json["pipelines"]["succeded_pipelines"] = success_pipeline
            self.repo_json["pipelines"]["failed_pipelines"] = failed_pipeline
            self.repo_json["pipelines"]["percent_succeded"] = percent_success

    # def generate_report(self, project_owner, project_name):
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": "Bearer " + self.GITLAB_API_TOKEN
    #     }
    #     # pegar o id
    #     project_id = self.get_project_id(project_owner, project_name)
    #     # pegar as outras info
    #     branches = self.get_branches(project_owner, project_name)
    #     commits = self.get_commits(project_owner, project_name)
    #     jobs = self.get_jobs(project_owner, project_name)
    #     members = self.get_members(project_owner, project_name)
    #     project = self.get_project(project_owner, project_name)
    #     pipeline_info = self.get_pipeline(project_owner, project_name)
    #     # retornar para a Ada
    #     return jsonify({
    #         "branches": branches,
    #         "commits": commits,
    #         "jobs": jobs,
    #         "members": members,
    #         "project": project,
    #         "pipeline_info": pipeline_info
    #     }), 200

    def get_project_id(self, project_owner, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_url = project_owner + "%2F" + project_name
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_url}"
                                    .format(project_url=project_url),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            requested_id = response.json()
            return requested_id


    def repo_informations(self, project_owner, project_name):

        self.get_branches(project_owner, project_name)
        self.get_members(project_owner, project_name)
        self.get_commits(project_owner, project_name)
        self.get_project(project_owner, project_name)
        self.get_pipeline(project_owner, project_name)
        generated_report = []
        generated_report.append(self.repo_json)
        return generated_report
