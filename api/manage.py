import coverage

from flask.cli import FlaskGroup

from gitlab import create_app
import unittest
import os
import sys
import subprocess


COV = coverage.coverage(
    branch=True,
    include='gitlab/*',
    omit=[
        'gitlab/tests/*',
        'gitlab/config.py',
    ]
)
COV.start()

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

def env_loader():
    variables = {
        'DB_URL': os.getenv('DB_URL', ''),
        'DB_NAME': os.getenv('DB_NAME', ''),
        'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN', '')
    }
    with open(os.path.join('cronjob','loaded-env.txt'), 'w') as f:
        for name in variables:
            f.write(f'{name}={variables[name]}\n')
        f.close()

def setup_cron():
    a = subprocess.call(['./entrypoint_cron.sh'])
    print(a, file=sys.stderr)

if __name__ == "__main__":
    env_loader()
    cli()
    setup_cron()