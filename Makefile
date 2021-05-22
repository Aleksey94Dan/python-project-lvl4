SHELL:=/usr/bin/env bash

install:
		poetry install
createsuperuser:
		poetry run python manage.py createsuperuser
run:
		poetry run python manage.py runserver
lint:
		poetry run flake8 user tasks
test:
		poetry run python manage.py test
check:
		poetry check
clean:
		find . -type f -name *.pyc -delete
		find . -type d -name __pycache__ -delete

.PHONY: install createsuperuser run lint check clean test
