import requests
from requests.exceptions import HTTPError
import json
import os
import telegram
from gitlab.data.user import User
from gitlab.utils.gitlab_utils import GitlabUtils


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")

class MonitorDomain(GitlabUtils):
    def __init__(self, chat_id):
        super().__init__(chat_id)

    def verify_domain(self):
        bot = telegram.Bot(token=ACCESS_TOKEN)
        user_list = User.objects(domain__ne = None)
        for user in user_list:
            status = requests.get(user.domain)
            if status == 200:
                pass
            else:
                status == 404:
                bot.send_message(chat_id=chat_id,
                                text="Seu domínio está fora do ar, "
                                "verifique o que pode ter ocorrido "
                                "para que os usuários possam usar "
                                "sua aplicação normalmente."
                                reply_markup=reply_markup)
    return
