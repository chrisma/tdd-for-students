import logging, os
import xml.etree.ElementTree as ET
# from sh import mvn, ErrorReturnCode

logging.basicConfig(level=logging.DEBUG) #logging.WARNING
log = logging.getLogger(__name__)

# pom_file = os.path.join(os.getcwd(), "pom.xml")
# log.debug("Using {pom_file}".format(pom_file))

# output = mvn("-f", pom_file, "-Dgroups=phones.secret.TaskTests", "test")

test_files_dir = os.getcwd()
test_file_prefix = "TEST-phones.secret."
test_file_suffix = ".xml"

def is_test_file(filename):
	return filename.startswith(test_file_prefix) and filename.endswith(test_file_suffix)

log.debug("Searching for test files in {dir}".format(dir=test_files_dir))
test_file_paths = [f for f in os.listdir(test_files_dir) if is_test_file(f)]

def get_fails_from_xml(path):
	out = []
	tree = ET.parse(path)
	root = tree.getroot()
	for testcase in root.findall('testcase'):
		fail = testcase.find('error')
		fail_type = 'error'
		if fail is None:
			fail = testcase.find('failure')
			fail_type = 'failure'
		if fail is not None:
			out.append({'class': testcase.get('classname'),
						'name': testcase.get('name'),
						'type': fail_type,
						'message': fail.get('message')})
	return out

for path in test_file_paths:
	fails = get_fails_from_xml(path)
	print(fails)

