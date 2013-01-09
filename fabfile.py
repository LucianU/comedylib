from contextlib import contextmanager as _contextmanager
import os

from fabric.api import env, run, cd, prefix, settings

env.proj_root = '~/'
env.proj_repo = 'ssh://hg@bitbucket.org/lucianu/comedylib/'
env.virtualenv = 'comedylib'
env.activate = 'workon %s' % env.virtualenv
env.forward_agent = True


def stag():
    """
    Staging connection information
    """
    env.hosts = ['comedylib@elbear.com']
    env.proj_dir = os.path.join(env.proj_root, 'stag_comedylib')
    env.branch = 'staging'
    env.settings = 'comedylib.settings.staging'


def prod():
    """
    Production connection information
    """
    env.hosts = ['comedylib@elbear.com']
    env.proj_dir = os.path.join(env.proj_root, 'comedylib')
    env.branch = 'default'
    env.settings = 'comedylib.settings.production'


@_contextmanager
def _virtualenv():
    """
    Changes to the proj_dir and activates the virtualenv
    """
    with cd(env.proj_dir):
        with prefix(env.activate):
            yield


def clone():
    """
    Clones the project from the central repository
    """
    run('hg clone %s %s' % (env.proj_repo, env.proj_dir))


def make_virtualenv():
    """
    Creates a virtualenv on the remote host
    """
    run('mkvirtualenv --no-site-packages %s' % env.virtualenv)


def update_reqs():
    """
    Makes sure all packages listed in requirements are installed
    """
    with _virtualenv():
        run('pip install -r requirements/production.pip')


def update_code():
    """
    Pulls the latest changes from the central repository
    """
    with cd(env.proj_dir):
        run('hg pull && hg up %s' % env.branch)


def setup_nginx():
    """
    Uses the nginx config file to setup a virtual host
    """
    pass


def restart_uwsgi():
    """
    Restarts uwsgi process
    """
    with _virtualenv():
        run('supervisorctl -c confs/production/supervisord.conf'
            ' restart uwsgi')


def start_supervisord():
    """
    Starts supervisord on the remote host
    """
    with _virtualenv():
        run('supervisord -c confs/production/supervisord.conf')


def syncdb():
    """
    Runs syncdb (along with any pending south migrations)
    """
    with _virtualenv():
        run('manage.py syncdb --migrate')


def deploy():
    """
    Creates or updates the project, runs migrations, installs dependencies.
    """
    first_deploy = False
    with settings(warn_only=True):
        if run('test -d %s' % env.proj_dir).failed:
            first_deploy = True
            clone()
        if run('test -d $WORKON_HOME/%s' % env.virtualenv).failed:
            make_virtualenv()

    update_code()
    update_reqs()
    syncdb()
    if first_deploy:
        start_supervisord()
    else:
        restart_uwsgi()
