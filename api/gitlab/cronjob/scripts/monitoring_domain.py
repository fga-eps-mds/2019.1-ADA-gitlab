from gitlab.utils.gitlab_utils import GitlabUtils
from gitlab.data.user import User


class MonitorDomain(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_all(self):
        list(db.User.find({})

    def get_users_domain(self, chat_id):
        user_domain = self.GITLAB_API_URL +\
              "user/{chat_id}/"\
              "domain"\
              .format(chat_id=chat_id)
        user_domain_json = self.get_request(user_domain)
        user_domain_dict = {"user_domain": []}
        for i, item in enumerate(user_domain_json):
                _data = {"name": 0}
            branches_data["name"] = branches_json[i]["name"]
            branches_dict["branches"].append(branches_data)
        return user_domain_dict


