export PYTHONPATH=$(shell pwd)/src/
export PYTHONDONTWRITEBYTECODE=1
export ENVIRONMENT=DEVELOPMENT

.PHONY=help

PROJECT_NAME=todo_api

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

###
# Dependencies section
###
dependencies: ## Install prd dependencies
	@poetry install --without dev

dev-dependencies: ## Install prd dependencies
	@poetry install


###
# Lint section
###
_flake8:
	@flake8 --show-source src/

_isort:
	@isort --diff --check-only src/

_black:
	@black --check src/ -l 79

_isort-fix:
	@isort .

_black_fix:
	@black . -l 79

_dead_fixtures:
	@pytest --dead-fixtures tests/

_mypy:
	@mypy src/

lint: _flake8 _isort _black _mypy _dead_fixtures   ## Check code lint
format-code: _isort-fix _black_fix ## Format code


###
# Tests section
###
test: clean ## Run tests
	@pytest -s -x tests/ -vvv

test-coverage: clean ## Run tests with coverage output
	@pytest . src --cov --cov-report term-missing

test-matching: clean ## Run tests by match ex: make test-matching k=name_of_test
	@pytest -s -k $(k) tests/ -vvv
