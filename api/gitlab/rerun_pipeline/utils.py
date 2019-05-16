import requests
from requests.exceptions import HTTPError
import json
import sys
import telegram


class RerunPipeline():

    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN

    def rerun_pipeline(self, project_id, pipeline_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.GITLAB_API_TOKEN
        }
        url = ("https://gitlab.com/api/v4/projects/"
               "{project_id}/pipelines/{pipeline_id}"
               "/retry".format(project_id=project_id,
                               pipeline_id=pipeline_id))
        try:
            response = requests.post(url="{url}".format(url=url),
                                     headers=headers)
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            restart_status = response.json()
            return restart_status

    def build_buttons(self, pipeline_id):
        buttons = []
        buttons.append(telegram.InlineKeyboardButton(
                text= "Sim",
                callback_data="quero reiniciar a pipeline " + str(pipeline_id)))

        buttons.append(telegram.InlineKeyboardButton(
                text= "Não"))
        button_array = [buttons]
        print(button_array, file=sys.stderr)
        # print(buttons, file=sys.stderr)
        # repo_names = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
        # print(repo_names, file=sys.stderr)
        return button_array
