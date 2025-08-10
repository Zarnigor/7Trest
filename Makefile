PYTHON=python
MANAGE=python manage.py

run:
	$(MANAGE) runserver

migrations:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

test:
	$(MANAGE) test

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

collectstatic:
	$(MANAGE) collectstatic --noinput

lint:
	flake8 .

todo:
	cat ToDo
