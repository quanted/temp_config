Environment variables for QED-CTS

Two main types:

	* docker_*.env -- docker-related environment variables
	* local_*.env -- local dev environment variables

Three types within docker and local env vars:

	* *_epa.env -- env vars when working within EPA network
	* *_outside.env -- env vars when working outside EPA network
	* *_prod.env -- env vars when deployed on production server

To run:

	* unix: . config/set_env_vars.sh config/*.env
	* windows: config\set_env_vars.bat, type *.env filename and hit enter.