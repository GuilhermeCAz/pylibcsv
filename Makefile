include .env
export

# python
.PHONY: dependencies
dependencies:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

.PHONY: requirements
requirements:
	pip-compile -o requirements.txt --strip-extras
	pip-compile -o requirements-dev.txt --strip-extras --extra=dev

.PHONY: help
help:
	@echo Available targets:
	@echo dependencies     : Install dependencies
	@echo requirements     : Compile requirements files
	@echo help             : Show this help message

.DEFAULT_GOAL := help