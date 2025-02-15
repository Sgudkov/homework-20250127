lint:
	poetry run  black log_analyzer.py
	poetry run  isort log_analyzer.py
	poetry run  mypy  log_analyzer.py

install:
	poetry install

test: install
	poetry run pytest

run:
	poetry run python log_analyzer.py
