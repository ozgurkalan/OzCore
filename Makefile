.PHONY: all 

all: version docs

help:
	@echo "Pre-publish actions"
	@echo "all: make all pre-publish actions":
	@echo "version: bump package version from latest tag"
	@echo "docs: prepare docs for publish"
	@echo "serve-docs: hot-reload serve docs"
	@echo "build-docs:build sphinx to see errors"

version:
	@poetry version $(shell dunamai from any)

docs:
	@echo "creating requirements.txt..."
	@poetry export -f requirements.txt -o docs/requirements.txt --with dev --without-hashes

serve-docs:
	@echo "hotreload and serve sphinx..."
	@sphinx-autobuild docs docs/_build/html --port 5555

build-docs:
	@echo "build sphinx to see error messages"
	@sphinx-build docs docs/_build/html
