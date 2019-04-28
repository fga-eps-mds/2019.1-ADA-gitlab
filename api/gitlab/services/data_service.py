import sys
from data.current_pipeline import CurrentPipeline
from data.general_information_pipelines import GeneralInformationPipelines
from data.project import Project
from data.user import User

import datetime


def create_user(username: str) -> User:
    user = User()
    user.username = username

    user.save()

    return user


def get_user(username: str) -> User:
    user = User.objects(username=username).first()
    return user


def add_project_user(project: Project, user: User) -> User:
    user.project_id.append(project.id)
    user.save()
    return user


def create_project(user: User, description: str, name: str, web_url: str, branches: list) -> Project:
    project = Project()
    project.user_id = user.id
    project.description = description
    project.name = name
    project.web_url = web_url
    project.branches = branches

    project.save()
    add_project_user(project, user)
    return project


def get_project(name: str) -> Project:
    project = Project.objects(name=name).first()
    return project


def create_general_information_pipeline(project: Project, number_of_pipelines: int, successful_pipelines: int) -> GeneralInformationPipelines:
    pipeline = GeneralInformationPipelines()
    pipeline.project_id = project.id
    pipeline.number_of_pipelines = number_of_pipelines
    pipeline.successful_pipelines = successful_pipelines

    pipeline.save()
    return pipeline


def get_general_information_pipeline(project: Project) -> GeneralInformationPipelines:
    pipeline = GeneralInformationPipelines.objects(
        project_id=project.id).first()
    return pipeline


def create_current_pipeline(name: str, jobs: list) -> CurrentPipeline:
    current_pipeline = CurrentPipeline()
    current_pipeline.name = name
    current_pipeline.jobs = jobs

    current_pipeline.save()
    return current_pipeline()


def get_current_pipeline(project: Project) -> CurrentPipeline:
    pipeline = get_general_information_pipeline(project)
    current_pipeline = CurrentPipeline.objects(pipeline_id=pipeline.id).all()

    return current_pipeline
