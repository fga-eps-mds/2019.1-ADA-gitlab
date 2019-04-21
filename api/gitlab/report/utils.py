import requests
from requests.exceptions import HTTPError
import json


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

*** Info necessaria para pegar essas info: id do project
'''

class Report():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

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

    def get_branches(self, project_id, headers):
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/repository/\
                                     branches"
                                    .format(project_id=project_id["id"]),
                                    headers=headers)
            branches = response.json()
            branches_names = []
            for i, item in enumerate(branches):
                names = {"name": 0}
                names["name"] = branches[i]["name"]
                branches_names.append(names)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            return branches_names

    def get_commits(self, project_id, headers):
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/repository/\
                                     commits".format(project_id=
                                     project_id["id"]), headers=headers)
            commits = response.json()
            filtered_commits = []
            keys = {"number_of_commits": 0,
                       "last_commit": {"title": 0,
                                       "author_name": 0,
                                       "author_email": 0,
                                       "authored_date": 0}}
            keys["last_commit"]["title"] = commits[0]["title"]
            keys["last_commit"]["author_name"] = commits[0]["author_name"]
            keys["last_commit"]["author_email"] = commits[0]["author_email"]
            keys["last_commit"]["authored_date"] = commits[0]["authored_date"]
            number_of_commits = 0
            for i, item in enumerate(commits):
                number_of_commits = number_of_commits + 1
            keys["number_of_commits"] = number_of_commits
            filtered_commits.append(keys)
            response.raise_for_status()
        except HTTPError as http_error:
                dict_error = {"status_code": http_error.response.status_code}
                raise HTTPError(json.dumps(dict_error))
            else:
                return filtered_commits

    def get_jobs(project_id, headers):
        pass # quantos jobs vamos pegar ?

    def get_members(project_id, headers):
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/\
                                     members".format(project_id=
                                     project_id["id"]), headers=headers)
            members = response.json()
            filtered_members = []
            for i, item in enumerate(members):
                keys = {"name": 0, "username": 0, "state": 0}
                keys["name"] = members[i]["name"]
                keys["username"] = members[i]["username"]
                keys["state"] = members[i]["state"]
                filtered_members.append(keys)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            return filtered_members

    def get_project(project_id, headers):
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}".
                                    format(project_id=project_id["id"]),
                                           headers=headers)
            project = response.json()
            filtered_project = []
            for i, item in enumerate(project):
                keys = {"name": 0, "path": 0, "description": 0, "web_url": 0}
                keys["name"] = project[i]["name"]
                keys["path"] = project[i]["path"]
                keys["description"] = project[i]["description"]
                keys["web_url"] = project[i]["web_url"]
                filtered_project.append(keys)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            return filtered_project

    def get_pipeline(project_id, headers):
        # ultima pipeline
        # desempenho do ultimo mes
        #try:
        #    response = requests.get("https://gitlab.com/api/"
        #                            "v4/projects/{project_id}/pipelines".
        #                            format(project_id=project_id["id"]),
        #                                   headers=headers)
        #    pipelines = response.json()
            pass

    def generate_report(self, project_owner, project_name):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        # pegar o id
        project_id = get_project_id(project_owner, project_name);
        # pegar as outras info
        branches = get_branches(project_id, headers)
        commits = get_commits(project_id, headers)
        jobs = get_jobs(project_id, headers)
        members = get_members(project_id, headers)
        projects = get_project(project_id, headers)
        pipeline_info = get_pipeline(project_id, headers)
        # retornar para a Ada
        return jsonify({
            "branches": branches,
            "commits": commits,
            "jobs": jobs,
            "members": members,
            "project": project,
            "pipeline_info": pipeline_info
        }), 200
