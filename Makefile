# docker
.PHONY: build
build:
	docker build -t libcsv .

.PHONY: run
run:
	docker run -it libcsv

.PHONY:	tests
tests:
	docker run -it libcsv /bin/sh -c "source /app/.venv/bin/activate && pytest"

.PHONY: clean
clean:
	docker rm libcsv -f
	docker rmi libcsv -f

# python
.PHONY: dependencies
dependencies:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

.PHONY: requirements
requirements:
	pip-compile -o requirements-dev.txt --extra=dev
	pip-compile -o requirements-test.txt --extra=test

.PHONY: help
help:
	@echo Available targets:
	@echo build            : Build image
	@echo run              : Run image
	@echo clean            : Clean image and build files
	@echo test             : Run tests
	@echo dependencies     : Install dependencies
	@echo requirements     : Compile requirements files
	@echo help             : Show this help message

.DEFAULT_GOAL := help