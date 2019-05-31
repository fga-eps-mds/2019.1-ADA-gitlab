from gitlab.utils.gitlab_utils import GitlabUtils


class Report(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_project(self, project_owner, project_name):
        url = "https://gitlab.com/"+project_owner+'/'+project_name
        project_dict = {"project": {
                        "name": project_name,
                        "web_url": url}
                        }
        return project_dict
