from contextlib import contextmanager as _contextmanager
import os

from fabric.api import env, run, cd, prefix, settings

# Using the interactive flag to have access to virtualenvwrapper
# commands which are sourced in .bashrc
env.shell = '/bin/bash -l -i -c'
env.proj_root = '~/'
env.proj_repo = 'ssh://hg@bitbucket.org/lucianu/comedylib/'
env.virtualenv = 'comedylib'
env.activate = 'workon %s' % env.virtualenv
env.forward_agent = True


def stag():
    """
    Staging connection information
    """
    env.hosts = ['comedylib@staging.comedylib.com']
    env.proj_dir = os.path.join(env.proj_root, 'comedylib')
    env.branch = 'solr-mobile'
    env.settings = 'comedylib.settings.staging'
    env.conf_path = 'confs/staging/'


def prod():
    """
    Production connection information
    """
    env.hosts = ['comedylib@elbear.com']
    env.proj_dir = os.path.join(env.proj_root, 'comedylib')
    env.branch = 'default'
    env.settings = 'comedylib.settings.production'
    env.conf_path = 'confs/production/'


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


def collect_static():
    """
    Runs the manage.py collectstatic command.
    """
    with _virtualenv():
        django_settings = 'DJANGO_SETTINGS_MODULE=%s' % env.settings
        run('%s ./manage.py collectstatic --noinput' % django_settings)


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
        config_file = os.path.join(env.conf_path, 'supervisord.conf')
        run('supervisorctl -c %s restart uwsgi' % config_file)


def start_supervisord():
    """
    Starts supervisord on the remote host
    """
    with _virtualenv():
        config_file = os.path.join(env.conf_path, 'supervisord.conf')
        run('supervisord -c %s' % config_file)


def restart_supervisord():
    """
    Restarts supervisord on the remote host
    """
    with _virtualenv():
        config_file = os.path.join(env.conf_path, 'supervisord.conf')
        run('supervisorctl -c %s reload' % config_file)


def syncdb():
    """
    Runs syncdb (along with any pending south migrations)
    """
    with _virtualenv():
        # Using --noinput because there is a signal connected to
        # user creation which creates profiles. The problem is that
        # the profiles table hasn't been created at this point, if
        # this is the first run of syncdb on this machine. The admin
        # user can be created afterwards
        django_settings = 'DJANGO_SETTINGS_MODULE=%s' % env.settings
        run('%s ./manage.py syncdb --noinput --migrate' % django_settings)


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
    collect_static()
    syncdb()
    if first_deploy:
        start_supervisord()
    else:
        restart_uwsgi()
