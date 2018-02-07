# coding:utf-8

from __future__ import with_statement
from fabric.api import cd,run,runs_once,settings,prompt


def hello(name="jj"):
    print("Hello {name}!".format(name=name))

def deploy():

    code_dir = '/data/test_django/weeks/Mook'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")


def say_hi():
    # 交互提示，类似于raw_input
    username = prompt('please specify username:')
    prompt('Specify favorivate choice:', 'choice', default=1, validate=int)


