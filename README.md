# Environment handling for QED

temp_config first looks through a set list of environments in server_configs.json, then
if a matching SERVER_NAME doesn't exist in that file, temp_config runs its original routine where it automatically determines the environment to use.

### Current environment files
	1. cgi_docker_*.env - environments for old cgi servers.
	2. local_dev.env - local development without docker, outside epa intranet.
	3. local_docker_dev.env - local development with docker, outside epa intranet.
	4. local_epa_dev.env - local development without docker, with epa intranet access.

### Adding a new environment

To add a new environment for server deployment, first add an entry to temp_config/server_configs.json file. Each entry has the following keys: SERVER_NAME, ENV, DESCRIPTION:

	+ SERVER_NAME - The server's name, which can be obtained from socket.gethostname() (				Python), $HOSTNAME (Linux), or %COMPUTERNAME% (Windows), and assumes
					local if neither exist.
	+ ENV - The .env filename to point to for the server name.
	+ DESCRIPTION - Brief summary of server (optional).

### Dynamically set env vars in python code:

	from temp_config.set_environment import DeployEnv

	runtime_env = DeployEnv()
	runtime_env.load_deployment_environment()  # set env vars based on network access

### To set .env with a shell script, run:

	+ Linux: . set_env_vars.sh env_filename.env
	+ Windows: set_env_vars.bat env_filename.env