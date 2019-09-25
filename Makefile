init-stash:
	docker run -u root --mount type=bind,source=$(shell pwd)/data/stash,destination=/var/atlassian/application-data/stash atlassian/stash chown -R daemon  /var/atlassian/application-data/stash
run-stash:
	docker run --mount type=bind,source=$(shell pwd)/data/stash,destination=/var/atlassian/application-data/stash --name="stash" -d -p 7990:7990 -p 7999:7999 atlassian/stash
delete-stash:
	docker stop stash
	docker rm stash
build:
	docker build -t migrator:latest .
tty:
	docker run --rm -it migrator:latest /bin/bash