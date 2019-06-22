FROM python:3.6

WORKDIR /cronjob

RUN apt-get update && apt-get -y install cron

ADD ./docker/cronjob.requirements.txt /cronjob/cronjob.requirements.txt

RUN pip install -r cronjob.requirements.txt

# Adiciona todos os scripts
ADD /api/gitlab/data /cronjob/
ADD /cronjob /cronjob/


# Habilita todos os scripts
RUN chmod +x entrypoint_cron.sh \
    update_project_model.sh \
    update_user_model.sh

RUN python env_loader.py

RUN /cronjob/update_user_model.sh && \
    /cronjob/update_project_model.sh

ADD /cronjob/crontab /etc/cron.d/domain-cron

RUN chmod 0644 /etc/cron.d/domain-cron
RUN crontab /etc/cron.d/domain-cron

CMD ["./entrypoint_cron.sh"]
