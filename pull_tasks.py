import logging
from sh import git, ErrorReturnCode, ErrorReturnCode_128
from sys import exit

logging.basicConfig(level=logging.INFO)

repo_path = "/home/christoph/git/tdd-for-students"
remote_name = "tasks"
remote_url = "https://github.com/hpi-swt2-exercise/java-tdd-challenge-tasks.git"

try:
	remote_add = git('-C', repo_path, "remote", "add", remote_name, remote_url)
	logging.info("Added remote '{remote}'.".format(remote=remote_name))
except ErrorReturnCode_128:
	logging.info("Remote '{remote}' already exists".format(remote=remote_name))
except ErrorReturnCode:
    logging.error("Unknown Error when adding remote")
    exit(1)

# import pdb; pdb.set_trace()