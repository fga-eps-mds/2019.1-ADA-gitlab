from gitlab.utils.gitlab_utils import GitlabUtils


class ReportBranches(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_branches(self, project_id):
        url = self.GITLAB_API_URL +\
              "projects/{project_id}/"\
              "repository/branches"\
              .format(project_id=project_id)
        branches_json = self.get_request(url)
        branches_dict = {"branches": []}
        for i, item in enumerate(branches_json):
            branches_data = {"name": 0}
            branches_data["name"] = branches_json[i]["name"]
            branches_dict["branches"].append(branches_data)
        return branches_dict
