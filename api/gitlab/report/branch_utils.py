from gitlab.report.report_json import report_dict
from gitlab.utils.gitlab_utils import GitlabUtils


class ReportBranches(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.repo = report_dict

    pipelines_ids = []

    def get_branches(self, project_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "repository/branches"\
              .format(project_id=project_id)
        branches_json = self.get_request(url)
        branch_name = {"name": []}
        for i, item in enumerate(branches_json):
            branch_name["name"].append(branches_json[i]["name"])
        self.repo["branches"]["name"] = branch_name["name"]
