import logging, os, sys, cgi
import xml.etree.ElementTree as ET
from github3 import GitHub
from requests import get

logging.basicConfig(level=logging.DEBUG) #logging.WARNING
logging.getLogger('github3').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
log = logging.getLogger(__name__)

test_file_prefix = "TEST-phones.secret."
test_file_suffix = ".xml"
test_files_dir = os.getcwd()
log.debug("Searching for test files in {dir}".format(dir=test_files_dir))

def is_test_file(filename):
	return filename.startswith(test_file_prefix) and filename.endswith(test_file_suffix)

def get_fail_from_files(paths):
	total_score = 0
	for path in paths:
		log.debug("Reading file '{path}'".format(path=path))
		tree = ET.parse(path)
		root = tree.getroot()
		# Keep track of test counts
		total_tests = int(root.get('tests'))
		log.debug("total tests: {count}".format(count=total_tests))
		failed_tests = int(root.get('failures')) + int(root.get('errors')) + int(root.get('skipped'))
		log.debug("non-green tests: {count}".format(count=failed_tests))
		total_score += total_tests - failed_tests
		log.debug("score for current file: {score}".format(score=total_score))
		for testcase in root.findall('testcase'):
			fail = testcase.find('error')
			typ = 'error'
			if fail is None:
				fail = testcase.find('failure')
				typ = 'failure'
			if fail is not None:
				name = testcase.get('name')
				message = fail.get('message')
				log.debug("'{typ}' in test '{name}'".format(typ=typ, name=name))
				return (name, message, total_score)
	log.debug("All tests passed! Yay :D")
	return (None, None, 0)

test_file_paths = [f for f in os.listdir(test_files_dir) if is_test_file(f)]
test_file_paths.sort()
log.debug("Found {count} files: {list}".format(count=len(test_file_paths), list=test_file_paths))

name, message, score = get_fail_from_files(test_file_paths)
if name is None:
	log.debug("No tickets to create, exiting...")
	sys.exit(0)
message = cgi.escape(message)
# TODO make xml parser not delete linebreaks
message = message.replace('\\n', '\n')

log.debug("Test failure: {name}, {m}".format(name=name, m=repr(message)))

# Create Github issue
gh_username = 'swt2public'
gh_password = 'wnjxeUn6pQpcnR4V'

log.debug("Logging in as {user}".format(user=gh_username))
github = GitHub(gh_username, gh_password)
log.debug("Ratelimit remaining: {rate}".format(rate=github.ratelimit_remaining))

# create_issue(owner, repository, title, body=None, assignee=None, milestone=None, labels=[])
# TRAVIS_REPO_SLUG (owner_name/repo_name)
# https://docs.travis-ci.com/user/environment-variables/
owner, repo = os.environ.get('TRAVIS_REPO_SLUG').split('/')
log.debug("Repo: {owner}/{repo}".format(owner=owner, repo=repo))

log.debug("Attempting to create issue...")
resp = github.create_issue(owner, repo, name, message)
log.debug("Created ticket: {resp}".format(resp=resp))

# Post results
log.debug("Attempting to post score...")
url = "https://tdd-chart.herokuapp.com/score/add?user={user}&score={score}"
resp = get(url.format(user=owner, score=score))
log.debug("TDD-chart response: {code}".format(code=resp.status_code))
