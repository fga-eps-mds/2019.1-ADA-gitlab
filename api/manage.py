import coverage

COV = coverage.coverage(
    branch=True,
    include='gitlab/*',
    omit=[
        'gitlab/tests/*',
        'gitlab/config.py',
    ]
)
COV.start()


from flask.cli import FlaskGroup

from gitlab import create_app
import unittest

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def test():
    """
    Roda testes sem coverage
    """
    tests = unittest.TestLoader().discover("gitlab/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('gitlab/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    cli()
