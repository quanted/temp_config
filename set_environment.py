import os
import sys
import logging
from dotenv import load_dotenv
import requests

logging.info("set_environment.py")


class DeployEnv(object):
	"""
	Class for determining deploy env for running
	QED-CTS, et al. with.
	"""

	def __init__(self, language=None):
		self.docker_hostname = os.environ.get('DOCKER_HOSTNAME')
		self.hostname = os.environ.get('HOSTNAME')
		self.test_url = os.environ.get('EPA_ACCESS_TEST_URL')
		# self.test_url = 'https://134.67.114.2'
		if not self.test_url:
			self.test_url = 'https://134.67.114.2'
		self.language = language  # default assumption is python, could be nodejs though

	def load_deployment_environment(self):
		"""
		Determines if QED-CTS components are being deployed
		inside/outside epa network, with/without docker, prod, etc.
		"""

		logging.info("DOCKER_HOSTNAME: {}".format(self.docker_hostname))
		logging.info("HOSTNAME: {}".format(self.hostname))

		_env_file = ''  # environment file name

		if self.hostname == "ord-uber-vm001" or self.hostname == "ord-uber-vm003":
			# deploy with docker_prod.env on cgi servers
			logging.info("Deploying on prod server...")
			_env_file = 'docker_prod.env'
			# self.read_env_file('docker_prod')

		else:
			# determine if inside or outside epa network
			internal_request = None
			try:
				# simple request to qed internal page to see if inside epa network:
				logging.info("Testing for epa network access..")
				internal_request = requests.get(self.test_url, verify=False, timeout=1)
			except Exception as e:
				logging.info("Exception making request to qedinternal server...")
				logging.info("User has no access to cgi servers at 134 addresses...")

			logging.info("Response: {}".format(internal_request))

			if internal_request and internal_request.status_code == 200:
				logging.info("Inside epa network...")
				if not self.docker_hostname:
					logging.info("DOCKER_HOSTNAME not set, assumming local deployment...")
					logging.info("Deploying with local epa environment...")
					# self.read_env_file('local_epa')
					_env_file = 'local_epa.env'
				else:
					logging.info("DOCKER_HOSTNAME: {}, Deploying with epa docker environment...")
					# self.read_env_file('docker_epa')
					_env_file = 'docker_epa.env'
			else:
				logging.info("Assuming outside epa network...")
				if not self.docker_hostname:
					logging.info("DOCKER_HOSTNAME not set, assumming local deployment...")
					logging.info("Deploying with local non-epa environment...")
					# self.read_env_file('local_outside')
					_env_file = 'local_outside.env'
				else:
					logging.info("DOCKER_HOSTNAME: {}, Deploying with non-epa docker environment...")
					# self.read_env_file('docker_outside')
					_env_file = 'docker_outside.env'

		logging.info("reading env file function...")
		return self.read_env_file(_env_file)

	def read_env_file(self, env_file):
		"""
		Loads .env file env vars to be access with os.environ.get
		"""
		# logging.info("Looking for .env file at {}".format(env_file))
		logging.info("env file: " + env_file)

		if self.language != "nodejs":
			# set env vars with python-dotenv
			dotenv_path = 'temp_config/' + env_file
			load_dotenv(dotenv_path)

		return env_file

if __name__ == '__main__':
	"""
	Handling calls to set_environment as main.
	Example case: called by nodejs
	"""

	additional_arg = sys.argv[1]
	if additional_arg == "nodejs":
		# return env vars to nodejs, print statements are read 
		# by nodejs via output stream
		runtime_env = DeployEnv("nodejs")
		print runtime_env.load_deployment_environment()  # sent to cts_nodejs via stdout
