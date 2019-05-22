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
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "pipelines/{pipeline_id}"\
              .format(project_id=project_id,
                      pipeline_id=pipeline_id)

        pipeline = self.get_request(url)
        try:
            response = requests.get("https://gitlab.com/api/v4/projects/"
                                    "{project_id}/pipelines/{pipeline_id}"
                                    .format(project_id=project_id,
                                            pipeline_id=pipeline_id),
                                    headers=self.headers)
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