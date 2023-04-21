VENV_DIR = venv
PIP = $(VENV_DIR)/bin/pip

# TODO make first start command
# 1. create todo_test database

# TODO setup commands
# --------------------------------------------------------------------------------------
# Migrations
# --------------------------------------------------------------------------------------
makemigrations:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head

# --------------------------------------------------------------------------------------
# Requirements
# --------------------------------------------------------------------------------------
install_dev_requirements:
	$(PIP) install -r requirements.dev.txt

install_requirements:
	$(PIP) install -r requirements.txt

compile_requirements:
	pip-compile requirements.in -o requirements.txt
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# Linters and formatters
# --------------------------------------------------------------------------------------
check:
	isort --check-only --diff .
	black --check .
	flake8
	mypy .

format:
	isort .
	find . -name '*.py' -not -path '*/$(VENV_DIR)/*' | xargs pyupgrade --py310-plus || true
	black .
