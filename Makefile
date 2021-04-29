SHELL:=/usr/bin/env bash

install:
		poetry install
createsuperuser:
		poetry run python manage.py createsuperuser
makemigrate:
		poetry run python manage.py makemigrations links
migrate:
		poetry run python manage.py migrate
run:
		poetry run python manage.py runserver
lint:
		poetry run flake8 page_loader tests
		poetry run mypy page_loader tests
build:
		poetry build
publish:
		poetry publish -r test

package-install:
		pip install --user dist/*.whl
check:
		poetry check

clean:
		find . -type f -name *.pyc -delete
		find . -type d -name __pycache__ -delete

.PHONY: install createsuperuser makemigrate migrate run lint build publish check clean