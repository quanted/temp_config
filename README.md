Environment variables for QED-CTS

Two main types:

	* docker_*.env -- docker-related environment variables
	* local_*.env -- local dev environment variables

Three types within docker and local env vars:

	* *_epa.env -- env vars when working within EPA network
	* *_outside.env -- env vars when working outside EPA network
	* *_prod.env -- env vars when deployed on production server

To manually set .env, run:

	* unix: . set_env_vars.sh filename.env
	* windows: config\set_env_vars.bat filename.env

Dynamically set env vars with python script:

	* From command line:

	python set_environment.py "nodejs" -- handles stdin/stdout from cts_nodejs calling python script for setting env vars (keeps logic for selecting .env file in one file, but still have to add execution of python script in cts_nodejs codebase).

	* From python:

	from temp_config.set_environment import DeployEnv
	runtime_env = DeployEnv()
	runtime_env.load_deployment_environment()