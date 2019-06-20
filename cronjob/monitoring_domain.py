import requests
import os
import telegram
from user import User

DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")


bot = telegram.Bot(token=ACCESS_TOKEN)
user_list = User.objects(domain__ne=None)
for user in user_list:
    req = requests.get(user.domain)
    if req.status_code == 404:
        bot.send_message(chat_id=user.chat_id,
                         text="Seu domínio está fora do ar, "
                              "verifique o que pode ter ocorrido "
                              "para que os usuários possam usar "
                              "sua aplicação normalmente.")
    else:
        pass