import mongoengine


def global_init():
    mongoengine.register_connection(alias='AdaBot', name='ada_GitLab')
