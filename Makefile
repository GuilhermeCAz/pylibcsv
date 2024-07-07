# build
.PHONY: build
build:
	docker build -t libcsv .

.PHONY: run
run:
	docker run -it --rm libcsv

.PHONY: clean
clean:
	rm -rf build/
	rm -f libcsv.c
	rm -f libcsv*.so
	docker rm libcsv -f
	docker rmi libcsv -f
	docker system prune --all --filter "until=1h" -f

# python
.PHONY: dependencies
dependencies:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

.PHONY: requirements
requirements:
	pip-compile -o requirements-dev.txt --strip-extras --extra=dev

.PHONY: help
help:
	@echo Available targets:
	@echo build            : Build image
	@echo run              : Run image
	@echo clean            : Clean image and build files
	@echo dependencies     : Install dependencies
	@echo requirements     : Compile requirements files
	@echo help             : Show this help message

.DEFAULT_GOAL := help