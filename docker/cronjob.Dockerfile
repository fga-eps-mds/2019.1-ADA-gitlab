FROM python:3.6

RUN apt-get update && apt-get -y install cron

ADD ./docker/cronjob.requirements.txt .

RUN pip install -r cronjob.requirements.txt

# Adiciona todos os scripts
ADD /cronjob .

# Habilita todos os scripts
RUN chmod +x entrypoint_cron.sh

RUN python env_loader.py

ADD /cronjob/crontab /etc/cron.d/domain-cron

RUN chmod 0644 /etc/cron.d/domain-cron
RUN crontab /etc/cron.d/domain-cron 

CMD ["./entrypoint_cron.sh"]
