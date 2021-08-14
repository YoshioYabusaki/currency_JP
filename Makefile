SHELL := /bin/bash

manage_py := python app/manage.py

runserver:
	$(manage_py) runserver 0:8000

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

showmigrations:
	$(manage_py) showmigrations

rabbitmq:
	sudo service rabbitmq-server start

worker:
	cd app && celery -A settings worker -l info --autoscale=6,0
	# cd app && celery -A settings worker -l info --concurrency 20

beat:
	cd app && celery -A settings beat -l info

venv:
	python3 -m venv env
