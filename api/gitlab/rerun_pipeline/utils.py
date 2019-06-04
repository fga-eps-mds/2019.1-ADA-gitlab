import requests
from requests.exceptions import HTTPError
import json
import telegram
from gitlab.utils.gitlab_utils import GitlabUtils


class RerunPipeline(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def rerun_pipeline(self, project_id, pipeline_id):
        try:
            url = self.GITLAB_API_URL + "projects/"\
                  "{project_id}/pipelines/{pipeline_id}"\
                  "/retry".format(project_id=project_id,
                                  pipeline_id=pipeline_id)
            response = requests.post(url=url,
                                     headers=self.headers)
            response.raise_for_status()
        except HTTPError as http_error:
            dict_error = {"status_code": http_error.response.status_code}
            raise HTTPError(json.dumps(dict_error))
        else:
            return {"status": "Pipeline Restarted"}

    def build_buttons(self, pipeline_id):
        buttons = []
        buttons.append(telegram.InlineKeyboardButton(
                text="Reiniciar pipeline",
                callback_data="quero reiniciar a pipeline " + str(pipeline_id))
                      )
        button_array = [buttons]
        return button_array
