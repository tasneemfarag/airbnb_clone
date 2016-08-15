from fabric.api import *
from fabric.contrib import *

''' Deploys codebase via github.com/rickharris-dev/microblog-project.git'''

env.shell = '/bin/bash -c'

def pack(remote="origin", branch="master"):
    ''' Updates github with local changes '''
    code_dir = '$HOME/airbnb_clone'

    with lcd(code_dir):
        ''' - Opted to not have fabric commit files to prevent unwanted code
            - Pull prevents errors during push, but may produce conflicts '''
        local("git pull " + remote + " " + branch)
        local("git push " + remote + " " + branch)

def setup_rick(repo="https://github.com/rickharris-dev/airbnb_clone.git"):
    env.hosts = ['admin@158.69.91.92', 'ubuntu@52.91.120.197']
    execute('setup')

def setup_tasneem(repo="https://github.com/rickharris-dev/airbnb_clone.git"):
    env.hosts = ['admin@158.69.85.206', 'ubuntu@54.173.6.112']
    execute('setup')

def deploy_rick(repo="https://github.com/rickharris-dev/airbnb_clone.git"):
    env.hosts = ['admin@158.69.91.92', 'ubuntu@52.91.120.197']
    execute('deploy')

def deploy_tasneem(repo="https://github.com/rickharris-dev/airbnb_clone.git"):
    env.hosts = ['admin@158.69.85.206', 'ubuntu@54.173.6.112']
    execute('deploy')

def setup(repo="https://github.com/rickharris-dev/airbnb_clone.git"):
    ''' Check if git is installed on the server '''
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show git')
    if result.failed is True:
        warn('Installing Git...')
        run('sudo apt-get install git')

    ''' Initializes the repository at the default location '''
    repo_dir = '/var'
    code_dir = '/var/airbnb_clone'
    git_dir = '/var/airbnb_clone/.git'

    if 'admin' in env.host_string:
        user = 'admin'
    else:
        user = 'ubuntu'

    with cd(repo_dir):
        if not files.exists('airbnb_clone'):
            run("sudo git clone " + repo)
            run("sudo chown -R " + user + ":" + user + " airbnb_clone")
        else:
            with cd(git_dir):
                remote = run("grep 'rickharris-dev/airbnb_clone.git' config")
                if not remote:
                    print 'Incorrect repository'
                else:
                    print 'Repository exists!'

def deploy(remote="origin", branch="master"):
    ''' Updates the production code '''

    code_dir = '/var/airbnb_clone'

    with cd(code_dir):
        run("git pull " + remote + " " + branch)
