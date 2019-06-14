import requests
import os
import telegram
import mongoengine
import sys

DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
db = mongoengine.connect(DB_NAME, host=DB_URL, alias='AdaBot')
User = db.User

print('#'*30, file=sys.stderr)
print('TESTE', file=sys.stderr)
print('#'*30, file=sys.stderr)
bot = telegram.Bot(token=ACCESS_TOKEN)
user_list = User.objects(domain__ne=None)
for user in user_list:
    status = requests.get(user.domain)
    if status == 404:
        bot.send_message(chat_id=user.chat_id,
                            text="Seu domínio está fora do ar, "
                            "verifique o que pode ter ocorrido "
                            "para que os usuários possam usar "
                            "sua aplicação normalmente.")
    else:
        pass
