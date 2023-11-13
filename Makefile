.PHONY: doc_server format install manage_migrations security server test

doc_server:
	@mkdocs serve --dev-addr '127.0.0.1:8001'
format:
	@isort .
	@blue .
install:
	@poetry install
manage_migrations:
	@python manage.py makemigrations
	@python manage.py migrate
security:
	@pip-audit
server:
	@python manage.py runserver
test:
	@pytest -v