import requests
from requests.exceptions import HTTPError
import json
from datetime import date
from datetime import datetime
from gitlab.report.report_json import report_dict
from gitlab.utils.gitlab_utils import GitlabUtils
import sys


class ReportPipelines(GitlabUtils):
    def __init__(self, GITLAB_API_TOKEN):
        super().__init__(GITLAB_API_TOKEN)
        self.repo = report_dict    
        self.pipelines_ids = []

    def get_pipeline(self, project_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "pipelines"\
              .format(project_id=project_id)


        pipelines = self.get_request(url)
        
        number_of_pipelines = 0
        success_pipeline = 0
        failed_pipeline = 0

        pipeline_days = {
            "last_7_days": {
                "number_of_pipelines": 0,
                "percent_succeded": 0,
                "percent_failed": 0,
                "succeded_pipelines": 0,
                "failed_pipelines": 0
            },
             "last_30_days": {}
            }
        pipeline_days['last_30_days'].update(pipeline_days['last_7_days'])

        for i, item in enumerate(pipelines):
            self.pipelines_ids.append(pipelines[i]["id"])
            is_recent = self.check_pipeline_date(
                project_id, pipelines[i]["id"])
            if is_recent["last_7_days"]:
                pipeline_days["last_7_days"]["number_of_pipelines"] += 1
                if pipelines[i]["status"] == "success":
                    pipeline_days["last_7_days"]["succeded_pipelines"] += 1
                    success_pipeline = success_pipeline + 1
                else:
                    pipeline_days["last_7_days"]["failed_pipelines"] += 1
                    failed_pipeline = failed_pipeline + 1
            elif is_recent["last_30_days"]:
                pipeline_days["last_30_days"]["number_of_pipelines"] += 1
                if pipelines[i]["status"] == "success":
                    pipeline_days["last_30_days"]["succeded_pipelines"] += 1
                    success_pipeline = success_pipeline + 1
                else:
                    pipeline_days["last_30_days"]["failed_pipelines"] += 1
                    failed_pipeline = failed_pipeline + 1
            elif pipelines[i]["status"] == "success":
                success_pipeline = success_pipeline + 1
            else:
                failed_pipeline = failed_pipeline + 1

        if pipeline_days["last_30_days"]["number_of_pipelines"]:
            pipeline_days["last_30_days"]["percent_succeded"] = (pipeline_days["last_30_days"]["succeded_pipelines"]/
                                                            pipeline_days["last_30_days"]["number_of_pipelines"]) * 100.0
            pipeline_days["last_30_days"]["percent_failed"] = 100 - pipeline_days["last_30_days"]["percent_succeded"]
        
        self.update_report_dict(pipeline_days, False)

        if pipeline_days["last_7_days"]["number_of_pipelines"]:
                pipeline_days["last_7_days"]["percent_succeded"] = (pipeline_days["last_7_days"]["succeded_pipelines"]/
                                                                pipeline_days["last_7_days"]["number_of_pipelines"]) * 100.0
                pipeline_days["last_7_days"]["percent_failed"] = 100 - pipeline_days["last_7_days"]["percent_succeded"]
        
        self.update_report_dict(pipeline_days, True)

        number_of_pipelines = len(pipelines)
        percent_success = (success_pipeline / number_of_pipelines) * 100.0
        statistics_dict = {
            "number_of_pipelines": number_of_pipelines,
            "succeded_pipelines": success_pipeline,
            "failed_pipelines": failed_pipeline,
            "percent_succeded": percent_success,
            "current_pipeline_id": pipelines[0]["id"],
            "current_pipeline_name": pipelines[0]["ref"]
            }
        self.update_report_statistics(statistics_dict)
    
    def update_report_dict(self, pipeline_days, seven_days=True):
        if seven_days:
            days_key = "last_7_days"
        else:
            days_key = "last_30_days"
        update_days = self.repo["pipelines"]["recents_pipelines"][days_key]
        for key in pipeline_days[days_key]:
            update_days[key] = pipeline_days[days_key][key]

    def update_report_statistics(self, statistics_dict):
        pipelines_statistics = self.repo["pipelines"]
        for key in statistics_dict:
            pipelines_statistics[key] = statistics_dict[key]

    def check_pipeline_date(self, project_id, pipeline_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "pipelines/{pipeline_id}"\
              .format(project_id=project_id,
                      pipeline_id=pipeline_id)

        pipeline = self.get_request(url)

        todays_date = date.today()
        pipeline_date = datetime.strptime(
            pipeline['created_at'][0:10], "%Y-%m-%d")
        pipeline_date = pipeline_date.date()
        qntd_days = todays_date-pipeline_date

        pipeline_qnt = {"last_7_days": None, "last_30_days": None}

        if qntd_days.days <= 7:
            pipeline_qnt["last_7_days"] = True
            
        elif qntd_days.days <= 30:
            pipeline_qnt["last_30_days"] = True
            
        return pipeline_qnt