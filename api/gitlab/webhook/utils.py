from flask import Blueprint, request, jsonify
from flask_cors import CORS
import os
import sys
from gitlab.data.user import User
from gitlab.data.project import Project
import json
from requests.exceptions import HTTPError


class Webhook():
    def register_repo(self, repo_data):
        project_name = repo_data["project_name"]
        chat_id = repo_data["chat_id"]
        project_id = repo_data["project_id"]

        user = User.objects(chat_id=chat_id).first()
        try:
            if user.project:
                dict_error = {"message":
                            "Eu vi aqui que você já tem um projeto cadastrado. "
                            "Sinto muito, mas no momento não é possível "
                            "cadastrar um projeto novo ou alterá-lo."}
                raise HTTPError(json.dumps(dict_error))
            project = Project()
            project.save_webhook_infos(user, project_name, project_id)
            user.save_gitlab_repo_data(user, project)
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
                          "Eu vi aqui que você já cadastrou o usuário do GitLab. "
                          "Sinto muito, mas no momento não é possível "
                          "cadastrar um novo usuário do GitLab "
                          "ou alterá-lo."}
            raise HTTPError(json.dumps(dict_error))
        user.save_gitlab_user_data(user, gitlab_user, chat_id, gitlab_user_id)
