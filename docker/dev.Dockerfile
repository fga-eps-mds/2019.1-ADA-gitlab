# base image
FROM python:3.6-slim

# set working directory
WORKDIR /usr/src/app

# install cronjob dependencies
RUN apt-get update && apt-get -y install nano \
    && apt-get -y install cron

# add and install requirements
ADD ./docker/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
ADD ./api /usr/src/app

ADD ./api/cronjob/crontab /etc/cron.d/domain-cron

RUN chmod 0644 /etc/cron.d/domain-cron
RUN crontab /etc/cron.d/domain-cron

# new
CMD python manage.py run -h 0.0.0.0