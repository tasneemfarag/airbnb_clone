from fabric.api import *
from fabric.contrib import *

''' Deploys codebase via github.com/rickharris-dev/microblog-project.git'''
env.shell = '/bin/bash -c'
rick_hosts = ('admin@158.69.91.92', 'ubuntu@52.91.120.197')
tasneem_hosts = ('admin@158.69.85.206', 'ubuntu@54.173.6.112')

def pack(remote="origin", branch="master"):
    ''' Updates github with local changes '''
    code_dir = '$HOME/airbnb_clone'

    with lcd(code_dir):
        ''' - Opted to not have fabric commit files to prevent unwanted code
            - Pull prevents errors during push, but may produce conflicts '''
        local("git pull " + remote + " " + branch)
        local("git push " + remote + " " + branch)

def deploy(dev="rick", local_code="$HOME/airbnb_clone/api", repo="https://github.com/rickharris-dev/airbnb_clone.git", remote='origin', branch='master'):
    with lcd(local_code):
        result = local('AIRBNB_ENV=test python -m unittest discover tests --pattern=*.py')
    if not result.failed:
        if dev == 'rick':
            execute(deploy_rick, repo, remote, branch)
        elif dev == 'tasneem':
            execute(deploy_tasneem, repo, remote, branch)

@hosts(rick_hosts)
def deploy_rick(repo, remote, branch):
    start_deploy(repo, remote, branch)

@hosts(tasneem_hosts)
def deploy_tasneem(repo, remote, branch):
    start_deploy(repo, remote, branch)

def start_deploy(repo, remote, branch):
    ''' Updates the production code '''
    ''' Check if git is installed on the server '''
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = run('sudo dpkg-query --show git')
        warn(result)
        if result.failed is True:
            setup(repo)

    code_dir = '/var/airbnb_clone'
    with cd(code_dir):
        run("sudo git pull " + remote + " " + branch)


def setup(repo="https://github.com/rickharris-dev/airbnb_clone.git"):
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
