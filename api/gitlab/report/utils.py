import requests
from requests.exceptions import HTTPError
import json
from flask import jsonify
import sys
from datetime import date
from datetime import datetime


'''
US30 - Informações para o relatório
Project Resources - https://docs.gitlab.com/ee/api/#project-resources

Nome do repo -> projects [ name ] --> ok

Branches --> ok
    -Name --> ok

Commits --> ok
    -Quantidade de commits (como ?) --> ok
    -Último commit --> ok
        -Title --> ok
        -Author_name --> ok
        -Author_email --> ok
        -Authored_date --> ok

Jobs
    -Status
    -Stage
    -Name
    -Ref
    -pipeline
        -Ref
        -Status
        -Web_url

Members from project , not from groups --> ok
    -Name --> ok
    -Username --> ok
    -State --> ok

Projects --> ok
    -Name --> ok
    -Description --> ok
    -web_url --> ok

Pipelines
    -number_of_pipelines --> ok
    -succeded --> ok
    -failed --> ok
    -succeded_percentage --> ok
    -Gráfico de sucesso de pipelines da última semana e último mês (imagem) ->\
        via método check_pipeline_date()

Current_pipeline --> ok
    -name --> ok
    -id --> ok
    -jobs --> ok
        -duration --> ok
        -Name --> ok
        -stage --> ok
        -status --> ok
        -web_url --> ok

Por quanto tempo os pipelines estão rodando?
    -Média de tempo de execução dos pipelines --> ok
    -Menor tempo de execução --> ok
    -Maior tempo de execução --> ok
    -Gráfico de tempo de execução

    # pegar todos os id das pipelines existentes, via api get pipelines --> ok
    # passar em cada pipeline e guardar a duracao --> ok

*** Info necessaria para pegar essas info: id do project
'''


class Report():
    pipelines_ids = []

    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
        self.repo_json = {"branches": {"name": 0}, "commits": {"last_commit": {"title": 0, "author_name": 0,
                                                                                                        "author_email": 0, "authored_date": 0}, "number_of_commits": 0},
                          "project": {"name": 0, "web_url": 0},
                          "pipelines": {"number_of_pipelines": 0, "succeded_pipelines": 0,
                                        "failed_pipelines": 0, "percent_succeded": 0, "current_pipeline_id": 0,
                                        "current_pipeline_name": 0, "recents_pipelines": {
                                            "last_7_days":{
                                                "number_of_pipelines":0,
                                                "percent_succeded": 0,
                                                "percent_failed" : 0,
                                                "succeded_pipelines": 0,
                                                "failed_pipelines": 0
                                            },
                                            "last_30_days":{
                                                "number_of_pipelines":0,
                                                "percent_succeded": 0,
                                                "percent_failed" : 0,
                                                "succeded_pipelines": 0,
                                                "failed_pipelines": 0
                                            }
                                        }
                                    }, "pipelines_times":
                            {"average": 0, "lower": 0, "higher": 0, "total": 0}}

    def get_branches(self, project_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/projects/{project_id}/repository/branches"
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
            self.repo_json["branches"]["name"] = branch_name["name"]

    def get_commits(self, project_id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }

        try:
            response = requests.get("https://gitlab.com/api/v4/projects/{project_id}/repository/commits".format(
                project_id=project_id), headers=headers)
            commits_json = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            number_of_commits = len(commits_json)
            self.repo_json["commits"]["last_commit"]["title"] = commits_json[0]["title"]
            self.repo_json["commits"]["last_commit"]["author_name"] = commits_json[0]["author_name"]
            self.repo_json["commits"]["last_commit"]["author_email"] = commits_json[0]["author_email"]
            self.repo_json["commits"]["last_commit"]["authored_date"] = commits_json[0]["authored_date"]
            self.repo_json["commits"]["number_of_commits"] = number_of_commits

    def get_project(self, project_owner, project_name):

            self.repo_json["project"]["name"] = project_name
            url = "https://gitlab.com/"+project_owner+'/'+project_name
            self.repo_json["project"]["web_url"] = url

            # print(self.repo_json, file=sys.stderr)

    def get_pipeline(self, project_id):
        '''Busca o numero de pipelines, quantas falharam, quantas passaram\
           e busca as pipelines da ultima semana e do ultimo mes, via \
           check_pipeline_date(), para montar um grafico'''
        # ultima pipeline
        # desempenho do ultimo mes
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/{project_id}/pipelines".format(
                project_id=project_id), headers=headers)
            pipelines = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            number_of_pipelines = 0
            success_pipeline = 0
            failed_pipeline = 0

            last_7_days = [0,0,0,0,0] # total, succeded, failed, percent succ, percent fail
            last_30_days = [0,0,0,0,0]# total, succeded, failed, percent succ, percent fail
            for i, item in enumerate(pipelines):
                # chamar a check_pipeline_date pra verificar a data da pipeline
                self.pipelines_ids.append(pipelines[i]["id"])
                is_recent = self.check_pipeline_date(
                    project_id, pipelines[i]["id"])
                if(is_recent[0]):
                    if(is_recent[1] == 7):
                        last_7_days[0]+=1
                        if(pipelines[i]["status"] == "success"):
                            last_7_days[1]+=1
                        else:
                            last_7_days[2]+=1
                    else:
                        last_30_days[0]+=1
                        if(pipelines[i]["status"] == "success"):
                            last_30_days[1]+=1
                        else:
                            last_30_days[2]+=1

                if pipelines[i]["status"] == "success":
                    success_pipeline = success_pipeline + 1
                else:
                    failed_pipeline = failed_pipeline + 1
            if(last_30_days[0]):
                last_30_days[3] = (last_30_days[1]/last_30_days[0])*100.0
                last_30_days[4] = 100 - last_30_days[3]
            self.repo_json["pipelines"]["recents_pipelines"]["last_30_days"]["number_of_pipelines"] = last_30_days[0]
            self.repo_json["pipelines"]["recents_pipelines"]["last_30_days"]["percent_succeded"] = last_30_days[3]
            self.repo_json["pipelines"]["recents_pipelines"]["last_30_days"]["percent_failed"] = last_30_days[4]
            self.repo_json["pipelines"]["recents_pipelines"]["last_30_days"]["succeded_pipelines"] = last_30_days[1]
            self.repo_json["pipelines"]["recents_pipelines"]["last_30_days"]["failed_pipelines"] = last_30_days[2]

            if(last_7_days[0]):
                last_7_days[3] = (last_7_days[1]/last_7_days[0])*100.0
                last_7_days[4] = 100 - last_7_days[3]
            self.repo_json["pipelines"]["recents_pipelines"]["last_7_days"]["number_of_pipelines"] = last_7_days[0]
            self.repo_json["pipelines"]["recents_pipelines"]["last_7_days"]["percent_succeded"] = last_7_days[3]
            self.repo_json["pipelines"]["recents_pipelines"]["last_7_days"]["percent_failed"] = last_7_days[4]
            self.repo_json["pipelines"]["recents_pipelines"]["last_7_days"]["succeded_pipelines"] = last_7_days[1]
            self.repo_json["pipelines"]["recents_pipelines"]["last_7_days"]["failed_pipelines"] = last_7_days[2]

            number_of_pipelines = len(pipelines)
            percent_success = (success_pipeline / number_of_pipelines) * 100.0
            self.repo_json["pipelines"]["number_of_pipelines"] = number_of_pipelines
            self.repo_json["pipelines"]["succeded_pipelines"] = success_pipeline
            self.repo_json["pipelines"]["failed_pipelines"] = failed_pipeline
            self.repo_json["pipelines"]["percent_succeded"] = percent_success
            self.repo_json["pipelines"]["current_pipeline_id"] = pipelines[0]["id"]
            self.repo_json["pipelines"]["current_pipeline_name"] = pipelines[0]["ref"]

    def check_pipeline_date(self, project_id, pipeline_id):
        '''Busca a data da pipeline referida em pipeline_id e verifica se ela \
           é da ultima semana ou do ultimo mes. Retorna true, se a pipeline \
           for do ultimo mes ou da ultima semana, false caso contrario'''
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/"
                                    "{project_id}/pipelines/{pipeline_id}".format
                                    (project_id=project_id,
                                     pipeline_id=pipeline_id), headers=headers)
            pipeline = response.json()
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            # checar a data da pipeline em pipeline["created_at"] e comparar
            # com a data atual
            # saber a data atual:
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

            # print(todays_date-pipeline_date, file=sys.stderr)
            # todays_date = datetime.strptime(todays_date, "%Y-%m-%d")
            # saber qual o ultimo mes e qual a ultima semana


    # def get_pipelines_times(self, project_id):
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": "Bearer " + self.GITLAB_API_TOKEN
    #     }
    #     pipelines_durations = []
    #     for i in self.pipelines_ids:
    #         try:
    #             response = requests.get("https://gitlab.com/api/v4/projects/{project_id}/pipelines/{current_pipeline_id}".format(
    #                 project_id=project_id, current_pipeline_id=i), headers=headers)
    #             pipeline = response.json()
    #             response.raise_for_status()
    #         except HTTPError as http_error:
    #             dict_error = {"status_code": http_error.response.status_code}
    #             raise HTTPError(json.dumps(dict_error))
    #         else:
    #             pipelines_durations.append(pipeline["duration"])
    #             pipelines_total_time = pipeline["duration"]
    #     # print(pipelines_durations, file=sys.stderr)
    #     # print(pipelines_total_time, file=sys.stderr)
    #     pipelines_average_time = pipelines_total_time / \
    #         (len(self.pipelines_ids))
    #     try:
    #         pipelines_lower_time = min(pipelines_durations)
    #         pipelines_higher_time = max(pipelines_durations)
    #     except TypeError:
    #         pipelines_lower_time = '{?}'
    #         pipelines_higher_time= '{?}'
    #     self.repo_json["pipelines_times"]["average"] = pipelines_average_time
    #     self.repo_json["pipelines_times"]["total"] = pipelines_total_time
    #     self.repo_json["pipelines_times"]["higher"] = pipelines_higher_time
    #     self.repo_json["pipelines_times"]["lower"] = pipelines_lower_time
    #     # print(pipelines_higher_time, file=sys.stderr)
    #     # graph
    #     # x = []
    #     # for i in self.pipelines_ids:
    #     #    x.append(i)
    #     # y = []
    #     # for i in pipelines_durations:
    #     #    y.append(i)
    #     # matplot.plot(x, y)
    #     # matplot.xlabel("Pipeline id")
    #     # matplot.ylabel("Time(s)")
    #     # graph = matplot.show()

    def repo_informations(self, user, project):

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        project_id = int(project.project_id)
        project_name = project.name
        project_owner = user.gitlab_user
        self.get_branches(project_id)
        self.get_commits(project_id)
        self.get_project(project_owner, project_name)
        self.get_pipeline(project_id)
        # self.get_pipelines_times(project_id)
        generated_report = []
        generated_report.append(self.repo_json)
        return generated_report
