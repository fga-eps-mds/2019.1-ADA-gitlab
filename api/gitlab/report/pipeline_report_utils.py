import requests
from requests.exceptions import HTTPError
import json
from datetime import date
from datetime import datetime
from gitlab.report.report_json import report_dict
from gitlab.utils.gitlab_utils import GitlabUtils
import sys


class ReportPipelines(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.repo = report_dict    
        self.pipelines_ids = []
        self.pipeline_days = {
            "last_7_days": {
                "number_of_pipelines": 0,
                "percent_succeded": 0,
                "percent_failed": 0,
                "succeded_pipelines": 0,
                "failed_pipelines": 0
            },
             "last_30_days": {}
        }
        self.pipeline_status = {
            "success_pipeline": 0,
            "failed_pipeline": 0,
        }

    def get_pipeline(self, project_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "pipelines"\
              .format(project_id=project_id)
        pipelines = self.get_request(url)        
        self.pipeline_days['last_30_days'].update(self.pipeline_days['last_7_days'])
        
        self.build_report(pipelines, project_id)
        self.build_pipeline_statistics("last_30_days")
        self.update_report_dict("last_30_days")
        self.build_pipeline_statistics("last_7_days")
        self.update_report_dict("last_7_days")

        number_of_pipelines = len(pipelines)
        percent_success = (self.pipeline_status["success_pipeline"] / number_of_pipelines) * 100.0
        statistics_dict = {
            "number_of_pipelines": number_of_pipelines,
            "succeded_pipelines": self.pipeline_status["success_pipeline"],
            "failed_pipelines": self.pipeline_status["failed_pipeline"],
            "percent_succeded": percent_success,
            "current_pipeline_id": pipelines[0]["id"],
            "current_pipeline_name": pipelines[0]["ref"]
            }
        self.update_report_statistics(statistics_dict)
    
    def update_report_dict(self, days_key):
        update_days = self.repo["pipelines"]["recents_pipelines"][days_key]
        for key in self.pipeline_days[days_key]:
            update_days[key] = self.pipeline_days[days_key][key]

    def update_report_statistics(self, statistics_dict):
        pipelines_statistics = self.repo["pipelines"]
        for key in statistics_dict:
            pipelines_statistics[key] = statistics_dict[key]

    def build_pipeline_dict(self, pipelines, i,
                            days_key):
        self.pipeline_days[days_key]["number_of_pipelines"] += 1
        if pipelines[i]["status"] == "success":
            self.pipeline_days[days_key]["succeded_pipelines"] += 1
            self.pipeline_status["success_pipeline"] =\
                 self.pipeline_status["success_pipeline"] + 1
        else:
            self.pipeline_days[days_key]["failed_pipelines"] += 1
            self.pipeline_status["failed_pipeline"] =\
                 self.pipeline_status["failed_pipeline"] + 1
    
    def build_pipeline_statistics(self, days_key):
        if self.pipeline_days[days_key]["number_of_pipelines"]:
            self.pipeline_days[days_key]["percent_succeded"] = (self.pipeline_days[days_key]["succeded_pipelines"]/
                                                            self.pipeline_days[days_key]["number_of_pipelines"]) * 100.0
            self.pipeline_days[days_key]["percent_failed"] = 100 - self.pipeline_days[days_key]["percent_succeded"]

    def build_report(self, pipelines, project_id):
        for i, item in enumerate(pipelines):
            self.pipelines_ids.append(pipelines[i]["id"])
            recent_pipelines = self.check_pipeline_date(
                project_id, pipelines[i]["id"])
            if recent_pipelines["last_7_days"]:
                self.build_pipeline_dict(pipelines, i, "last_7_days")
            elif recent_pipelines["last_30_days"]:
                self.build_pipeline_dict(pipelines, i, "last_30_days")
            elif pipelines[i]["status"] == "success":
                self.pipeline_status["success_pipeline"] = self.pipeline_status["success_pipeline"] + 1
            else:
                self.pipeline_status["failed_pipeline"] = self.pipeline_status["failed_pipeline"] + 1
    

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