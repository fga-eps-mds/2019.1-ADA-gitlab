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
    -http_url_to_repo

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

    def generate_report(self, project_owner, project_name):
        # pegar o id
        project_id = get_project_id(project_owner, project_name);
        # pegar as outras info
        branches = get_branches(project_id)
        commits = get_commits(project_id)
        jobs = get_jobs(project_id)
        members = get_members(project_id)
        projects = get_projects(project_id)
        # retornar para a Ada 
        return jsonify({
            "branches": branches,
            "commits": commits,
            "jobs": jobs,
            "members": members,
            "projects": projects
        }), 200
