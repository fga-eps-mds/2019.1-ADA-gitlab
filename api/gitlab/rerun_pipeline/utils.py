import requests
from requests.exceptions import HTTPError
import json
from datetime import date
from datetime import datetime


class RerunPipeline():

    def __init__(self, GITLAB_API_TOKEN):
        self.GITLAB_API_TOKEN = GITLAB_API_TOKEN
