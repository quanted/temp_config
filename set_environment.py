import os
import sys
import logging
from dotenv import load_dotenv
import requests
import json

logging.warning("set_environment.py")



class ServerConfig:
    """
    Handles server configurations that are laid out in
    the server_config.json file.
    """

    def __init__(self):

        self.server_configs_file = "temp_config/server_configs.json"  # filename for server configs
        self.current_config = None  # env var file to load
        self.configs = []  # var for list of config objects from general json config
        self.read_json_config_file()  # loads server config json to configs attribute

    def read_json_config_file(self):
        """
        Reads in general json config as object, sets
        configs attribute.
        """
        with open(self.server_configs_file, 'r') as config_file:
            config_json = config_file.read()
            self.configs = json.loads(config_json)
        return True

    def get_config(self, search_key, search_val):
        """
        Searches above configs by IP or HOSTNAME depending
        on search_key, and compares with search_val. Returns
        env var file name to load.
        """
        for config_obj in self.configs:
            if config_obj[search_key] == search_val:
                self.current_config = config_obj["ENV"]
                return self.current_config

    def set_current_config(self, ip=None, hostname=None):
        """
        Sets config environment based on above configs. Returns
        env var file to load based on IP or HOSTNAME.
        """
        if ip:
            self.current_config = self.get_config("IP", ip)
        elif hostname:
            self.current_config = self.get_config("HOSTNAME", hostname)
        else:
            self.current_config = None

        return self.current_config



class DeployEnv(ServerConfig):
    """
    Class for determining deploy env for running QED apps.
    """

    def __init__(self):

        ServerConfig.__init__(self)

        # Env vars used to determine server config:
        self.docker_hostname = os.environ.get('DOCKER_HOSTNAME')  # docker hostname (set in docker-compose)
        self.hostname = os.environ.get('HOSTNAME')  # server hostname env var
        self.ip = os.environ.get('IP')  # server ip env var

        # Test URL for determining if server is within EPA intranet:
        self.epa_access_test_url = 'https://qedinternal.epa.gov'
        if not self.epa_access_test_url:
            self.epa_access_test_url = 'https://qedinternal.epa.gov'
        
        self.env_path = "temp_config/environments/"  # path to .env files


    def load_deployment_environment(self):
        """
        Looks through server_configs.json with ServerConfig class,
        then, if there's not a matching config, tries to automatically
        determine what .env file to use.
        """

        logging.warning("DOCKER_HOSTNAME: {}".format(self.docker_hostname))
        logging.warning("HOSTNAME: {}".format(self.hostname))
        logging.warning("IP: {}".format(self.ip))

        env_filename = ''  # environment file name

        # Runs ServerConfig's func to get env file based on ip and/or hostname:
        env_filename = self.set_current_config(self.ip, self.hostname)
    
        if not env_filename:
            # Tries to automatically set environment:
            env_filename = self.run_auto_env_selector()

        logging.warning("loading env vars from: {}".format(env_filename))

        dotenv_path = self.env_path + env_filename  # sets .env file path

        load_dotenv(dotenv_path)  # loads env vars into environment

        return env_filename


    def run_auto_env_selector(self):
        """
        Routine that tries determine what .env file to use automatically.
        Makes call to qedinternal to check if deployed in epa intranet, and
        checks for DOCKER_HOSTNAME env var to determine if docker or not.
        """
        # determine if inside or outside epa network
        internal_request = None
        try:
            # simple request to qed internal page to see if inside epa network:
            logging.warning("Testing for epa network access..")
            internal_request = requests.get(self.epa_access_test_url, verify=False, timeout=1)
        except Exception as e:
            logging.warning("Exception making request to qedinternal server...")
            logging.warning("User has no access to cgi servers at 134 addresses...")

        logging.warning("Response: {}".format(internal_request))

        if internal_request and internal_request.status_code == 200:
            logging.warning("Inside epa network...")
            if not self.docker_hostname:
                logging.warning("DOCKER_HOSTNAME not set, assumming local deployment...")
                logging.warning("Deploying with local epa environment...")
                return 'local_epa_dev.env'
            else:
                return 'cgi_docker_dev.env'
        else:
            logging.warning("Assuming outside epa network...")
            if not self.docker_hostname:
                logging.warning("DOCKER_HOSTNAME not set, assumming local deployment...")
                logging.warning("Deploying with local non-epa environment...")
                return 'local_dev.env'
            else:
                logging.warning("DOCKER_HOSTNAME: {}, Deploying with non-epa docker environment...")
                return 'local_docker_dev.env'

        return None