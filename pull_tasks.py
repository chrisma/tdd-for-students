import logging, os
from sh import git, ErrorReturnCode, ErrorReturnCode_1, ErrorReturnCode_128
from sys import exit

logging.basicConfig(level=logging.DEBUG) #logging.WARNING
logging.getLogger('sh').setLevel(logging.WARNING)
log = logging.getLogger(__name__)

remote_name = "tasks"
remote_url_https = "https://github.com/hpi-swt2-exercise/java-tdd-challenge-tasks.git"
remote_url_ssh = "git@github.com:hpi-swt2-exercise/java-tdd-challenge-tasks.git"
repo_path = os.getcwd()

log.debug("Running git commands in {path}".format(path=repo_path))

log.debug("Attempting to add git remote...")
try:
	remote_add = git("-C", repo_path, "remote", "add", remote_name, remote_url_ssh)
	log.debug("Added remote '{remote}'".format(remote=remote_name))
except ErrorReturnCode_128:
	log.debug("Remote '{remote}' already exists".format(remote=remote_name))
except ErrorReturnCode:
	log.error("Unknown error when adding '{remote}' remote".format(remote=remote_name))
	exit(1)

log.debug("Attempting to extract current branch...")
try:
	current_branch = git("-C", repo_path, "symbolic-ref", "--short", "-q", "HEAD")
	current_branch = current_branch.strip('\n')
	log.debug("Currently on branch '{branch}'".format(branch=current_branch))
except ErrorReturnCode_1:
	log.error("Error when checking for current branch. Probably in 'detached HEAD' mode")
	exit(1)
except ErrorReturnCode:
	log.error("Unknown error when checking for current branch")
	exit(1)

log.debug("Pulling remote '{remote}' into branch {branch}, overwriting local changes...".format(
	remote=remote_name, branch=current_branch))
try:
	git("-C", repo_path, "pull", "-X", "theirs", remote_name, current_branch)
except ErrorReturnCode:
	log.error("Error pulling from remote '{remote}'".format(remote=remote_name))

try:
	latest_commit = git("rev-parse", "HEAD").strip('\n')
	log.debug("Latest commit is now {hash}".format(hash=latest_commit))
except ErrorReturnCode:
	log.error("Error getting the lastest commit")

# import pdb; pdb.set_trace()