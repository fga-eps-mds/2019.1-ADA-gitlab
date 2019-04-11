# api/gitlab/manage.py


from flask.cli import FlaskGroup

from gitlab import app
import unittest


cli = FlaskGroup(app)


@cli.command()
def test():
    """
    Roda testes sem coverage
    """
    tests = unittest.TestLoader().discover('gitlab/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
