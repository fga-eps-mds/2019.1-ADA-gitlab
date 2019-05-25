# api/gitlab/__init__.py

import requests
from requests.exceptions import HTTPError
import json
import os
import telegram
import sys

class UserUtils():
    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def get_project_user(self, project_owner):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        user_id = self.get_user_id(project_owner)
        if not user_id:
            dict_error = {"status_code": 404}
            raise HTTPError(json.dumps(dict_error))
        try:
            response = requests.get("https://gitlab.com/api/"
                                    "v4/users/{user_id}/projects"
                                    .format(
                                        user_id=user_id
                                    ),
                                    headers=headers)
            response.raise_for_status()
        except IndexError as index_error:
            dict_error = {"status_code": 404}
            index_error.message = json.dumps(dict_error)
        else:
            requested_user = response.json()
            return requested_user

    def get_user_id(self, project_owner):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        try:
            response = requests.get("https://gitlab.com/api/v4/users?username="
                                    "{project_owner}"
                                    .format(project_owner=project_owner),
                                    headers=headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        except IndexError:
            print("#"*60, file = sys.stderr)
            print(index_error, file = sys.stderr)
            dict_error = {"status_code": 404}
            raise IndexError(json.dumps(dict_error))
            
        else:
            requested_id = response.json()
            return requested_id[0]["id"]

    def get_user(self):
        headers = {
            "Content-Type": "applications/json"
        }
        user_url = "https://gitlab.com/api/v4/user?"\
                   "access_token={access_token}"\
                   .format(access_token=self.GITLAB_API_TOKEN)
        response = requests.get(url=user_url, headers=headers)
        requested_user = response.json()
        gitlab_data = {
                       "gitlab_username": requested_user["username"],
                       "gitlab_user_id": requested_user["id"]
                      }
        return gitlab_data

    def send_message(self, token, chat_id):
        access_token = os.environ.get("ACCESS_TOKEN", "")
        bot = telegram.Bot(token=access_token)
        bot.send_message(chat_id=chat_id,
                         text="Você foi cadastrado com sucesso no GitLab")

    def select_repos_by_buttons(self, project_owner, headers):
        headers = {
            "Content-Type": "applications/json"
        }
        get_repository = "http://localhost:5000/user/{project_owner}".format(
                project_owner=project_owner)
        response = requests.get(
            url=get_repository, headers=headers)

        received_repositories = response.json()
        buttons = []
        for repositorio in received_repositories["repositories"]:
            project_name = repositorio.split('/')
            project_name = project_name[-1]
            buttons.append(telegram.InlineKeyboardButton(
                text=project_name,
                callback_data="meu repositorio do gitlab é " + repositorio))
        repo_names = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        return repo_names
