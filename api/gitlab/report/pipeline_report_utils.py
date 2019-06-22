from gitlab.report.report_json import report_dict
from gitlab.utils.gitlab_utils import GitlabUtils
import sys


class ReportPipelines(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.repo = report_dict
        self.pipelines_ids = []
        self.pipeline_status = {
            "success_pipeline": 0,
            "failed_pipeline": 0,
            "another_status": 0
        }
        self.last_50_pipelines = {
                "another_status": 0,
                "percent_succeded": 0,
                "percent_failed": 0,
                "succeded_pipelines": 0,
                "failed_pipelines": 0
        }
        self.last_pipelines = 50

    def get_pipeline(self, project_id):
        i = 0
        pipelines = []
        print("#"*30, file=sys.stderr)
        while True:
            i += 1
            url = self.GITLAB_API_URL +\
                "projects/{project_id}/"\
                "pipelines?per_page=100&page={i}"\
                .format(project_id=project_id,
                        i=i)
            response = self.get_request(url)
            for item in response:
                pipelines.append(item)
            if len(response) < 100:
                break

        print(pipelines[0], file=sys.stderr)
        if not pipelines:
            statistics_dict = {
                "number_of_pipelines": 0,
                "succeded_pipelines": 0,
                "failed_pipelines": 0,
                "another_status": 0,
                "percent_succeded": 0,
                "percent_failed": 0,
                "current_pipeline_id": 0,
                "current_pipeline_name": 0
            }
        else:
            self.build_report(pipelines, project_id)
            number_of_pipelines = len(pipelines)
            percent_success = (self.pipeline_status["success_pipeline"]
                               / number_of_pipelines) * 100.0
            percent_failed = (self.pipeline_status["failed_pipeline"]
                              / number_of_pipelines) * 100.0
            number_of_last_pipelines = self.last_pipelines
            if len(pipelines) < self.last_pipelines:
                number_of_last_pipelines = len(pipelines)
            self.last_50_pipelines["percent_succeded"] = format(
                (100.0 * self.last_50_pipelines["succeded_pipelines"]
                 / number_of_last_pipelines), '.2f')
            self.last_50_pipelines["percent_failed"] = format(
                (100.0 * self.last_50_pipelines["failed_pipelines"]
                 / number_of_last_pipelines), '.2f')
            statistics_dict = {
                "number_of_pipelines": number_of_pipelines,
                "succeded_pipelines": self.pipeline_status["success_pipeline"],
                "failed_pipelines": self.pipeline_status["failed_pipeline"],
                "another_status": self.pipeline_status["another_status"],
                "percent_succeded": round(percent_success, 2),
                "percent_failed": round(percent_failed, 2),
                "current_pipeline_id": pipelines[0]["id"],
                "current_pipeline_name": pipelines[0]["ref"],
                "50_last": self.last_50_pipelines
                }
        pipeline_dict = {"pipeline": 0}
        pipeline_data = self.update_report_statistics(statistics_dict)
        pipeline_dict["pipeline"] = pipeline_data
        return pipeline_dict

    def update_report_statistics(self, statistics_dict):
        pipelines_statistics = self.repo["pipelines"]
        for key in statistics_dict:
            pipelines_statistics[key] = statistics_dict[key]
        return pipelines_statistics

    def build_report(self, pipelines, project_id):
        for i, item in enumerate(pipelines):
            self.pipelines_ids.append(pipelines[i]["id"])
            if pipelines[i]["status"] == "success":
                self.pipeline_status["success_pipeline"] = (self.
                                                            pipeline_status
                                                            ["success_"
                                                             "pipeline"] + 1)
                if i < 50:
                    self.last_50_pipelines["succeded_pipelines"] += 1
            elif pipelines[i]["status"] == "failed":
                self.pipeline_status["failed_pipeline"] = (self.
                                                           pipeline_status
                                                           ["failed_"
                                                            "pipeline"] + 1)
                if i < 50:
                    self.last_50_pipelines["failed_pipelines"] += 1
            else:
                self.pipeline_status["another_status"] = (self.
                                                          pipeline_status
                                                          ["another_status"
                                                           ] + 1)
                if i < 50:
                    self.last_50_pipelines["another_status"] += 1
