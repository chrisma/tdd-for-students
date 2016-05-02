import logging
from sh import git, ErrorReturnCode, ErrorReturnCode_128
from sys import exit

logging.basicConfig(level=logging.DEBUG) #logging.WARNING
logging.getLogger('sh').setLevel(logging.WARNING)

repo_path = "."
remote_name = "tasks"
remote_url_https = "https://github.com/hpi-swt2-exercise/java-tdd-challenge-tasks.git"
remote_url_ssh = "git@github.com:hpi-swt2-exercise/java-tdd-challenge-tasks.git"
local_branch = "master"

logging.debug("Attempting to add git remote...")
try:
	remote_add = git("-C", repo_path, "remote", "add", remote_name, remote_url_ssh)
	logging.debug("Added remote '{remote}'".format(remote=remote_name))
except ErrorReturnCode_128:
	logging.debug("Remote '{remote}' already exists".format(remote=remote_name))
except ErrorReturnCode:
    logging.error("Error when adding '{remote}' remote".format(remote=remote_name))
    exit(1)

logging.debug("Pulling remote '{remote}', overwriting local changes...".format(remote=remote_name))
try:
	git("-C", repo_path, "pull", "-X", "theirs", remote_name, local_branch)
except ErrorReturnCode:
	logging.error("Error pulling from remote '{remote}'".format(remote=remote_name))

# import pdb; pdb.set_trace()