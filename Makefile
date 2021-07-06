SHELL:=/usr/bin/env bash

install:
		poetry install
createsuperuser:
		poetry run python manage.py createsuperuser
run:
		poetry run python manage.py runserver
migrate:
		poetry run python manage.py migrate
lint:
		poetry run flake8 user statuses labels tasks utils
test:
		poetry run python manage.py test --parallel
check:
		poetry check
clean:
		find . -type f -name *.pyc -delete
		find . -type d -name __pycache__ -delete

.PHONY: install createsuperuser run lint check clean test
