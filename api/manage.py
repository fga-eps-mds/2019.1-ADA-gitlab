# services/users/manage.py


from flask.cli import FlaskGroup

from gitlab import app  # new


cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()