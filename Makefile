VENV_DIR = venv
PIP = $(VENV_DIR)/bin/pip

install_dev_requirements:
	$(PIP) install -r requirements.dev.txt

install_requirements:
	$(PIP) install -r requirements.txt

check:
	isort --check-only --diff .
	black --check .
	flake8
	mypy .

format:
	isort .
	black .