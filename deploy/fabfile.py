import time
from fabric.api import run, execute, env, cd

"""
Manage auto-deploy webhooks remotely.

Production hook:

  forever start -l $HOME/hookshot.log -a deploy/hookshot.js -p 4000 -b production -c "cd $HOME/production/current && git pull && bundle exec jekyll build >> $HOME/hookshot.log"
  forever restart deploy/hookshot.js -p 4000 -b production -c "cd $HOME/production/current && git pull && bundle exec jekyll build >> $HOME/hookshot.log"
  forever stop deploy/hookshot.js -p 4000 -b production -c "cd $HOME/production/current && git pull && bundle exec jekyll build >> $HOME/hookshot.log"
"""

environment = "production"
branch = "master"
port = 4000

env.use_ssh_config = True

home = "/home/site"
log = "%s/hookshot.log" % home
current = "%s/%s/current" % (home, environment)

# principal command to run upon update
command = "cd %s && git pull && bundle exec jekyll build >> %s" % (current, log)

def start():
  run(
    "cd %s && forever start -l %s -a deploy/hookshot.js -p %i -b %s -c \"%s\""
    % (current, log, port, branch, command)
  )

def stop():
  run(
    "cd %s && forever stop deploy/hookshot.js -p %i -b %s -c \"%s\""
    % (current, port, branch, command)
  )

def restart():
  run(
    "cd %s && forever restart deploy/hookshot.js -p %i -b %s -c \"%s\""
    % (current, port, branch, command)
  )
