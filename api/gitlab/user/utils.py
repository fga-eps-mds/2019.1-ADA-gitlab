# api/gitlab/__init__.py


from requests import post
import json
import os
import telegram
from telegram import Bot
from gitlab.data.user import User
from gitlab.utils.gitlab_utils import GitlabUtils

APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")
GITLAB_REDIRECT_URI = os.getenv("REDIRECT_URI", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


class UserUtils(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def get_user_project(self):
        url = self.GITLAB_API_URL + "/projects?membership=true"
        projects = super(UserUtils, self).get_request(url)
        return projects

    def get_user_id(self, project_owner):
        url = self.GITLAB_API_URL +\
              "users?username="\
              "{project_owner}"\
              .format(project_owner=project_owner)
        user_id = super(UserUtils, self).get_request(url)
        try:
            return user_id[0]["id"]
        except IndexError:
            return None

    def get_user_domain(self):
        user = User.objects(chat_id=self.chat_id).first()
        return user.domain

    def get_own_user_data(self):
        url = self.GITLAB_API_URL + \
              "user"

        requested_user = self.get_request(url)
        gitlab_data = {
                       "gitlab_username": requested_user["username"],
                       "gitlab_user_id": requested_user["id"]
                      }
        return gitlab_data

    def select_repos_by_buttons(self):
        repo_infos = self.get_user_project()
        repositories = []
        for item in repo_infos:
            repositories.append(item["path_with_namespace"])
        buttons = []
        for repositorio in repositories:
            project_name = repositorio.split('/')
            project_name = project_name[-1]
            buttons.append(telegram.InlineKeyboardButton(
                text=project_name,
                callback_data="meu repositorio do gitlab é " + repositorio))
        repo_names = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        return repo_names

    def send_button_message(self, user_infos, chat_id):
        bot = Bot(token=ACCESS_TOKEN)
        repo_names = self.select_repos_by_buttons()
        reply_markup = telegram.InlineKeyboardMarkup(repo_names)
        bot.send_message(chat_id=chat_id,
                         text="Encontrei esses repositórios na sua "
                         "conta do GitLab. Qual você quer que eu "
                         "monitore? Clica nele!",
                         reply_markup=reply_markup)
        return "OK"


def authenticate_access_token(code):
    header = {"Content-Type": "application/json"}
    redirect_uri = GITLAB_REDIRECT_URI
    data = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    url = "https://gitlab.com/oauth/token"
    data = json.dumps(data)
    post_response = post(url=url,
                         headers=header,
                         data=data)
    post_json = post_response.json()
    GITLAB_TOKEN = post_json['access_token']
    return GITLAB_TOKEN


def send_message(token, chat_id):
    bot = Bot(token=ACCESS_TOKEN)
    bot.send_message(chat_id=chat_id,
                     text="Você foi "
                     "cadastrado com "
                     "sucesso no GitLab")
    return "OK"
