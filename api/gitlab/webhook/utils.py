from gitlab.data.user import User
from gitlab.data.project import Project
import json
from requests.exceptions import HTTPError
import os
import requests


GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


class Webhook():
    def register_repo(self, repo_data):
        project_name = repo_data["project_name"]
        chat_id = repo_data["chat_id"]
        project_id = repo_data["project_id"]

        user = User.objects(chat_id=chat_id).first()
        try:
            if user.project:
                dict_error = {"message":
                              "Eu vi aqui que você já tem um projeto "
                              "cadastrado. Sinto muito, mas no momento "
                              "não é possível cadastrar um projeto novo "
                              "ou alterá-lo."}
                raise HTTPError(json.dumps(dict_error))
            project = Project()
            project.save_webhook_infos(user, project_name, project_id)
            user.save_gitlab_repo_data(project)
        except AttributeError:
            dict_error = {"message":
                          "Tive um erro tentando cadastrar seu repositório. "
                          "Mais tarde você tenta. Ok?"}
            raise AttributeError(json.dumps(dict_error))

    def register_user(self, user_data):
        user = User()
        gitlab_user = user_data["gitlab_user"]
        chat_id = user_data["chat_id"]
        gitlab_user_id = user_data["gitlab_user_id"]
        existing_user = User.objects(chat_id=chat_id).first()
        if existing_user:
            dict_error = {"message":
                          "Eu vi aqui que você já cadastrou o usuário "
                          "do GitLab. Sinto muitos, mas no momento não "
                          "é possível cadastrar um novo usuário do GitLab "
                          "ou alterá-lo."}
            raise HTTPError(json.dumps(dict_error))
        user.save_gitlab_user_data(gitlab_user, chat_id, gitlab_user_id)

    def get_pipeline_infos(self, project_id, pipeline_id):
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + GITLAB_API_TOKEN}
        response = requests.get("https://gitlab.com/api/"
                                "v4/projects/{project_id}/pipelines/"
                                "{pipeline_id}/jobs".format(
                                        project_id=project_id,
                                        pipeline_id=pipeline_id),
                                headers=headers)
        response.raise_for_status()
        resp = response.json()
        requested_build = []
        for i, item in enumerate(resp):
            job_data = {"job_id": 0, "branch": 0,
                        "commit": 0, "stage": 0,
                        "job_name": 0, "status": 0,
                        "web_url": 0}
            job_data["job_id"] = resp[i]["id"]
            job_data["branch"] = resp[i]["ref"]
            job_data["commit"] = resp[i]["commit"]["title"]
            job_data["stage"] = resp[i]["stage"]
            job_data["job_name"] = resp[i]["name"]
            job_data["status"] = resp[i]["status"]
            job_data["web_url"] = resp[i]["web_url"]
            job_data["pipeline_url"] = resp[i]["pipeline"]["web_url"]
            requested_build.append(job_data)
        return requested_build

    def build_message(self, job_build):
        jobs_message = "Os passos da build são:\n"

        for i, item in enumerate(job_build):
            if job_build[i]["status"] == "success":
                status = "✅"
            elif job_build[i]["status"] == "failed":
                status = "❌"
            else:
                status = "🔄"

            jobs_message += "{status} {job_name}\n"\
                            .format(status=status,
                                    job_name=job_build[i]["job_name"])

        summary_message = "A build #{job_id} "\
                          "da branch {branch}, "\
                          "commit {commit}, "\
                          "está no estágio de {stage}."\
                          .format(job_id=job_build[0]["job_id"],
                                  branch=job_build[0]["branch"],
                                  commit=job_build[0]["commit"],
                                  stage=job_build[0]["stage"])
        return {"jobs_message": jobs_message,
                "summary_message": summary_message}

    def build_status_message(self, content, jobs):
        if content["object_attributes"]["status"] == "success":
            status_message = "Muito bem! Um novo pipeline (de id #{id} "\
                             "da branch {branch}) terminou com sucesso. "\
                             "Se você quiser conferí-lo, "\
                             "o link é {link}".format(
                                id=content["object_attributes"]["id"],
                                branch=content["object_attributes"]["ref"],
                                link=jobs[0]["web_url"])
        elif content["object_attributes"]["status"] == "failed":
            status_message = "Poxa.. Um novo pipeline (de {id} e "\
                             "{branch}) falhou. Se você "\
                             "quiser conferí-lo, o link é {link}".format(
                                id=content["object_attributes"]["id"],
                                branch=content["object_attributes"]["ref"],
                                link=jobs[0]["web_url"])
        else:
            return "OK"
        return status_message
