# base image
FROM python:3.6-alpine

# set working directory
WORKDIR /usr/src/app

# add and install requirements
ADD ./docker/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
ADD . /usr/src/app

# new
CMD python manage.py run -h 0.0.0.0
