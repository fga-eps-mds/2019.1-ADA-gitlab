from gitlab.utils.gitlab_utils import GitlabUtils
from gitlab.report.branch_utils import ReportBranches
from gitlab.report.commit_utils import ReportCommits
from gitlab.report.pipeline_report_utils \
     import ReportPipelines


class Report(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.pipeline = ReportPipelines(chat_id)
        self.branches = ReportBranches(chat_id)
        self.commits = ReportCommits(chat_id)

    def get_project(self, project_owner, project_name):
        url = "https://gitlab.com/" + project_name
        project_dict = {"project": {
                        "name": project_name,
                        "web_url": url}
                        }
        return project_dict

    def get_data(self, kind, chat_id):
        if kind == "pipelines":
            return self.pipeline.return_project(
                                chat_id,
                                self.pipeline.check_project_exists,
                                self.pipeline)
        elif kind == "commits":
            return self.commits.return_project(
                            chat_id,
                            self.commits.check_project_exists,
                            self.commits)
        else:
            return self.branches.return_project(
                            chat_id,
                            self.branches.check_project_exists,
                            self.branches)
